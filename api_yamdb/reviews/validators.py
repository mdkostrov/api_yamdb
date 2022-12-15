from django.core.exceptions import ValidationError
from re import fullmatch


def username_validator(value):
    if value == 'me':
        raise ValidationError(
            'Имя пользователя не может быть <me>.',
            params={'value': value},
        )
    if fullmatch(r'[\w.@+_-]+', value) is None:
        raise ValidationError(
            'В имени пользователя допускаются только '
            'буквы, цифры и @/./+/-/_ знаки.',
            params={'value': value},
        )
    return value
