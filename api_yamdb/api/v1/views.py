from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.filters import TitleFilter
from api.v1.mixins import ListCreateDestroyMixin
from api.v1.pagination import PagePagination
from api.v1.permissions import (IsAdmin, IsAdminOrRead, IsAdminUpdate,
                                IsAuthor, IsModerator)
from api.v1.serializers import (CategoriesSerializer, CommentSerializer,
                                GenresSerializer, ReviewSerializer,
                                TitleReadSerializer, TitleSerializer,
                                TokenSerializer, UserCreateSerializer,
                                UserSerializer)
from reviews.models import Categories, Genres, Review, Title, User
from api_yamdb.settings import DOMAIN_NAME

FROM_EMAIL = f'noreply@{DOMAIN_NAME}'


class UserViewSet(ModelViewSet):
    """Класс для работы с моделью User с учетом разрешений.
    Имя me зарезервировано для обработки запросов пользователей о себе."""
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    pagination_class = PagePagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['patch', 'get'],
        detail=False,
        url_path='me',
        url_name='me',
        permission_classes=[IsAuthenticated]
    )
    def get_me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


class RegistrationView(APIView):
    """Класс для обработки запросов регистрации и получения токенов.
    Повторный запрос на апи с данными существующего пользователя возвращает
    новый код подтверждения."""
    permission_classes = (AllowAny,)
    http_method_names = ['post', ]

    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                email=request.data['email'],
            )
            data = {
                'username': user.username,
                'email': user.email,
            }
        except (KeyError, MultiValueDictKeyError, User.DoesNotExist):  # noqa
            serializer = UserCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            data = serializer.data
        token = default_token_generator.make_token(user)
        user.confirmation_code = token
        user.save()

        email_body = (
            f'Код подтверждения регистрации: {token}'
        )
        message = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Подтверждение регистрации'
        }
        self.send_email(message)
        return Response(data, status=status.HTTP_200_OK)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']],
            from_email=FROM_EMAIL,
        )
        email.send()


class GetTokenView(APIView):
    """Класс для поступающих запросов кода подтверждения.
     Запрос с парой username/email обрабатывается и высылает
     новый код подтверждения регистрации."""
    permission_classes = (AllowAny,)
    http_method_names = ('post',)

    def post(self, request):  # noqa
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )


class GenresViewSet(ListCreateDestroyMixin):
    """Класс для обработки запросов о жанрах."""
    queryset = Genres.objects.all()  # noqa
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrRead,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoriesViewSet(ListCreateDestroyMixin):
    """Класс для обработки запросов о категориях."""
    queryset = Categories.objects.all()  # noqa
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrRead,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """Класс для обработки запросов о произведениях.
    Подсчитывает средний рейтинг произведения при обращении.
    Разрешается использование фильтра при запросе."""
    queryset = Title.objects.all().annotate(  # noqa
        Avg('reviews__score')
    ).order_by('name')
    permission_classes = (IsAdminOrRead, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    """Класс для обработки запросов об отзывах на произведение.
    Ключ произведения передается в строке запроса."""
    serializer_class = ReviewSerializer
    http_method_names = ('get', 'patch', 'delete', 'post')
    permission_classes = [IsAuthor | IsModerator | IsAdminUpdate]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """Класс для обработки запросов о комментариях на отзывы.
        Ключ отзыва передается в строке запроса."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor | IsModerator | IsAdminUpdate]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
