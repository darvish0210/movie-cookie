from django.urls import path, include
from .views import PostViewSet, CommentViewSet, CommentOnlyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"view/comments", CommentOnlyViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"", PostViewSet)

urlpatterns = [path("", include(router.urls))]
