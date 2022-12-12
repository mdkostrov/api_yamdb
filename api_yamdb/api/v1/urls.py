from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import UserViewSet

router = DefaultRouter()
router.register(
    r'users',
    UserViewSet,
    basename='users'
)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
