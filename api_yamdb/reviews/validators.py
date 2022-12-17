from datetime import date
from re import fullmatch

from django.core.exceptions import ValidationError


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


def slug_validator(value):
    if fullmatch(r'^[-a-zA-Z0-9_]+$', value) is None:
        raise ValidationError(
            'В уникальном идентификаторе допускаются только'
            'буквы, цифры и _/- знаки.',
            params={'value': value},
        )
    return value


def year_validator(value):
    year = date.today().year
    if value > year:
        raise ValidationError('Год выпуска не может '
                              'быть больше текущего!')

    return value
