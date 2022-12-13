from abc import ABC

from rest_framework import serializers

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


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )
