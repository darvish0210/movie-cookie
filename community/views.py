from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, PostOnlySerializer
from rest_framework import viewsets, permissions, filters


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id", "title", "content"]
    filterset_fields = ["id", "title", "content"]
    ordering = ["id"]
    ordering_fields = ["id", "title", "content"]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def perform_create(self, serializer):
    #     return serializer.save(user=self.request.user)


class CommentOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostOnlySerializer
    # permission_classes = [permissions.AllowAny]
