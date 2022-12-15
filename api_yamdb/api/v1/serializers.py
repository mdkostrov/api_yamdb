from rest_framework import serializers

from reviews.validators import username_validator
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
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
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        return username_validator(value)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )
