
from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path("test/", testEndPoint, name="test"),
    path("profile/", getUserProfile, name="profile"),
    path("listusers/", listUsers, name="listusers"),
    path("deluser/<int:pk>", delUser, name="deluser"),
    path('', getRoutes)
]