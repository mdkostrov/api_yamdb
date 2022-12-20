from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                          GetTokenView, RegistrationView, ReviewViewSet,
                          TitleViewSet, UserViewSet)

v1_router = DefaultRouter()
v1_router.register(
    r'users',
    UserViewSet,
    basename='users',
)
v1_router.register(
    r'genres',
    GenresViewSet,
    basename='genres',
)
v1_router.register(
    r'categories',
    CategoriesViewSet,
    basename='categories',
)
v1_router.register(
    r'titles',
    TitleViewSet,
    basename='titles',
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

app_name = 'api'

urlpatterns = [
    path('auth/signup/', RegistrationView.as_view(), name='signup'),
    path('auth/token/', GetTokenView.as_view(), name='token'),
    path('', include(v1_router.urls)),
]
