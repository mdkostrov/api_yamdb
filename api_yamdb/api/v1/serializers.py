from rest_framework import serializers
from reviews.models import Categories, Genres, Title, User
from reviews.validators import (slug_validator, username_validator)


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
        if not user.role == 'admin':
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

    def validate_username(self, value): # noqa
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
    class Meta:
        model = Genres
        fields = ('name', 'slug')

    def validate_slug(self, value): # noqa
        return slug_validator(value)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')


    def validate_slug(self, value): # noqa
        return slug_validator(value)


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id',
                  'name', 'year', 'description',
                  'genre', 'category', 'rating',)


class TitleSerializer(serializers.ModelSerializer):
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
