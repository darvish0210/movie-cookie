from django.urls import path
from .views import signup_view, profile_view, profile_edit, delete_view

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    path("delete/<int:user_id>/", delete_view, name="delete_account"),
]
