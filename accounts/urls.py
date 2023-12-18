from django.urls import path, include
from . import views
from .views import profile_edit
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 로그인
    path("login/", views.login_view, name="login"),
    # 로그아웃
    path("logout/", views.logout_view, name="logout"),
    # 회원가입
    path("signup/", views.signup_view, name="signup"),
    # 프로필
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    # 회원탈퇴
    path("delete/<int:user_id>/", views.delete_view, name="delete_account"),
    # jwt
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
