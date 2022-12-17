from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class ListCreateDestroyMixin(ListModelMixin, CreateModelMixin,
                             DestroyModelMixin, GenericViewSet):
    """Кастомный миксин на основе базовых классов,
       дабы отключить использование непредусмотренных запросов"""
    pass
