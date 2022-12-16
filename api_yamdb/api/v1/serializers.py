from rest_framework import serializers

from reviews.models import User
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

    def validate_username(self, value):
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
