from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Categories, Comment, Genres, Review, Title, User
from reviews.validators import username_validator


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User.
    Пользователям запроещено изменять поле Role."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def update(self, instance, validated_data):
        if 'role' not in self.initial_data:
            return super().update(instance, validated_data)
        user = self.context['request'].user
        if not user.is_admin:
            validated_data.pop('role')
        return super().update(instance, validated_data)


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор работает с моделью User в части auth-запросов."""
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):  # noqa
        return username_validator(value)


class TokenSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с полем токен модели User."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )


class GenresSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с моделью Genres"""
    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с моделью Category"""
    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с моделью Title в части получения данных."""
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = ('id',
                  'name', 'year', 'description',
                  'genre', 'category', 'rating',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с моделью Title в части изменения данных."""
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name', 'year', 'description',
            'genre', 'category', 'rating',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с моделью Review."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError(
                'Нельзя оставлять несколько отзывов на одно произведение!'
            )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'title', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с моделью Comment."""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')
