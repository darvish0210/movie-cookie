# recommend/permissions.py
from rest_framework.permissions import BasePermission


class RecommendPermission(BasePermission):
    def has_permission(self, request, view):
        """
        `/recommend/`: 로그인 한 유저들만 DB에 저장된 추천영화 목록 조회(`GET`), DB에 저장(`POST`) 가능\n
        `/recommend/generate/`: 로그인 여부 상관없이 영화 추천받기(`POST`) 가능
        """
        if view.action == "generate":
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        `/recommend/<int:pk>/`: 본인의 추천영화 객체에만 조회(`GET`), 수정(`PATCH`), 삭제(`DELETE`) 가능
        """
        return obj.user == request.user
