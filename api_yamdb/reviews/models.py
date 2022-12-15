from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.validators import username_validator

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE_CHOICES = [
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER),
]


class User(AbstractUser):
    """Кастомная модель пользователя"""
    username = models.CharField(
        'Имя пользователя',
        validators=(username_validator,),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=False,
    )
    bio = models.TextField(
        'Био',
        blank=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=150,
        blank=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
