# recommend/permissions.py
from rest_framework.permissions import BasePermission


class RecommendPermission(BasePermission):
    # /recommend/: 로그인 한 유저들만 DB에 저장된 추천영화 목록 조회(GET), DB에 저장(POST) 가능
    # /recommend/generate/: 로그인 여부 상관없이 추천영화 생성(POST) 가능
    def has_permission(self, request, view):
        if view.action == "generate":
            return True
        return request.user.is_authenticated

    # /recommend/<int:pk>/: 본인의 추천영화에만 접근(GET), 수정(PATCH), 삭제(DELETE) 가능
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
