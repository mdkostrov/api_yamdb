from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.v1.permissions import IsAuthorOrSAFE
from api.v1.serializers import UserSerializer
from titles.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
