
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
    path("upduser/<int:pk>", UpdUser.as_view(), name="upduser"),
    path("getusergroups/", getUserGroups),
    ## Groups ##
    path("groups/", ListGroups.as_view()),
    path("addgroup/", CreateGroup.as_view()),
    path("groups/<int:pk>/", DetailGroup.as_view()),
    path("updgroup/<int:pk>/", UpdateGroup.as_view()),
    path("delgroup/<int:pk>/", DeleteGroup.as_view()),
    ## Permissions ##
    path("permissions/", ListPermissions.as_view()),
    path("permissions/<int:pk>/", DetailPermission.as_view()),
    path('', getRoutes)
]
