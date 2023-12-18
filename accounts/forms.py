from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(label="프로필 사진", required=False)

    class Meta:
        model = UserProfile
        fields = ["nickname", "tag", "introduction", "profile_picture"]


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="사용자 아이디", max_length=30)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]
