from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken


from api.v1.permissions import IsAdmin, IsModerator, IsUser
from api.v1.serializers import UserSerializer, UserCreateSerializer, TokenSerializer
from api.v1.pagination import PagePagination
from reviews.models import User


class UserViewSet(ModelViewSet):
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
    permission_classes = (AllowAny,)
    http_method_names = ['post', ]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = default_token_generator.make_token(user)
        user.confirmation_code = token
        user.save()

        email_body = (
            f'Код подтверждения регистрации: {token}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Подтверждение регистрации'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()


class GetTokenView(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ('post',)

    def post(self, request):
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
