from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


def signup_view(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data["username"]

            # 중복된 사용자 이름 확인
            if User.objects.filter(username=username).exists():
                # 이미 존재하는 사용자 이름일 경우 에러 메시지를 사용자에게 보여주고 다시 회원가입 페이지로 이동
                return render(
                    request,
                    "accounts/signup.html",
                    {
                        "user_form": user_form,
                        "profile_form": profile_form,
                        "error": "이미 존재하는 사용자 이름입니다.",
                    },
                )

            password = user_form.cleaned_data["password1"]
            # 프로필사진 저장안되서 수정중
            # user = User.objects.create_user(
            #     username, password=password, email=user_form.cleaned_data["email"]
            # )

            # profile = profile_form.save(commit=False)
            # profile.user_id = user.id
            # profile.save()
            user = User.objects.create_user(
                username, password=password, email=user_form.cleaned_data["email"]
            )

            # 사용자가 저장된 후에 ID를 가져와서 프로필에 할당
            user_id = user.id

            profile = profile_form.save(commit=False)
            profile.user_id = user_id
            profile.save()

            profile_form = UserProfileForm(
                request.POST, request.FILES, instance=profile
            )
            if profile_form.is_valid():
                profile_form.save()

            login(request, user)
            return redirect("login")

    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "accounts/signup.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("user_id")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "로그인되었습니다.")
            return redirect("profile")
        else:
            messages.error(request, "로그인에 실패하였습니다.")
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "로그아웃되었습니다.")
    return redirect("login")


@login_required
@require_POST
def delete_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user == user:
        user.delete()
        logout(request)
        messages.success(request, "계정이 삭제되었습니다.")
        return redirect("login")
    else:
        return HttpResponseForbidden(
            "Forbidden: You do not have permission to perform this action."
        )


@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "accounts/profile.html", {"user": user, "form": form})


@login_required
def profile_edit(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 성공적으로 수정되었습니다.")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "accounts/profile_edit.html", {"form": form})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def obtain_jwt_token(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    data = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    profile = user.profile

    form = UserProfileForm(request.data, request.FILES, instance=profile)
    if form.is_valid():
        form.save()
        return Response({"detail": "프로필이 성공적으로 수정되었습니다."}, status=status.HTTP_200_OK)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
