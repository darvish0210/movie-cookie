from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, UserProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST


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
                    "accounts_signup/signup.html",
                    {
                        "user_form": user_form,
                        "profile_form": profile_form,
                        "error": "이미 존재하는 사용자 이름입니다.",
                    },
                )

            password = user_form.cleaned_data["password1"]
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
        "accounts_signup/signup.html",
        {"user_form": user_form, "profile_form": profile_form},
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

    return render(request, "accounts_signup/profile.html", {"user": user, "form": form})


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

    return render(request, "accounts_signup/profile_edit.html", {"form": form})


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
