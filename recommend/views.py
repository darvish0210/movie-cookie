# recommend/views.py
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .models import Recommend
from .permissions import RecommendPermission
from .serializers import RecommendSerializer


class RecommendViewSet(ModelViewSet):
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer
    permission_classes = [RecommendPermission]

    # 해당 유저의 객체만 조회
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    # 추천 영화 생성하는 함수
    @action(detail=False, methods=["post"])
    def generate(self, request):
        pass
