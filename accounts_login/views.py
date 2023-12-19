from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect


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
    return render(request, "accounts_login/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "로그아웃되었습니다.")
    return redirect("login")
