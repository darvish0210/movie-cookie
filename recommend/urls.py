# recommend/urls.py
from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.RecommendViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
