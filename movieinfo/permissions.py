from rest_framework import permissions
from .models import OneLineCritic
from accounts.models import LikeMovie, WatchedMovie, WatchlistMovie


class OneLineCriticIsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 해당 한 줄평의 작성자에게만 허용
        return obj.author == request.user

    def has_permission(self, request, view):
        # 작성자가 아닌 경우 수정 권한 없음
        if request.method in ["PUT", "PATCH"]:
            if "pk" in view.kwargs:
                one_line_critic = OneLineCritic.objects.get(id=view.kwargs["pk"])
                return one_line_critic.author == request.user
        return True
