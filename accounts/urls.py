from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserCreateView, UserProfileViewSet

router = DefaultRouter()
router.register(r"user-profile", UserProfileViewSet, basename="user-profile")

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("signup/", UserCreateView.as_view(), name="signup"),
    path("api/", include(router.urls)),
]
