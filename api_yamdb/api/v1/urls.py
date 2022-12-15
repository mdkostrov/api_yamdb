from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import  RegistrationView, GetTokenView, UserViewSet

router = DefaultRouter()
router.register(
    r'users',
    UserViewSet,
    basename='users',
)

# router.register(
#     r'users/me',
#     UserGetPatchListViewSet,
#     basename='users-detail',
# )


app_name = 'api'

urlpatterns = [
    path('auth/signup/', RegistrationView.as_view(), name='signup'),
    path('auth/token/', GetTokenView.as_view(), name='token'),
    path('', include(router.urls)),
]
