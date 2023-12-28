from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    LikeMovieSerializer,
    WatchedMovieSerializer,
    WatchlistMovieSerializer,
)
from django.contrib.auth import get_user_model
from .permissions import IsOwnerOrReadOnly
from .models import LikeMovie, WatchedMovie, WatchlistMovie

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return super().get_permissions()


class LikedMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        liked_movies = LikeMovie.objects.filter(user=request.user)
        serializer = LikeMovieSerializer(liked_movies, many=True)
        return Response(serializer.data)


class WatchedMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        watched_movies = WatchedMovie.objects.filter(user=request.user)
        serializer = WatchedMovieSerializer(watched_movies, many=True)
        return Response(serializer.data)


class WatchlistMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        watchlist_movies = WatchlistMovie.objects.filter(user=request.user)
        serializer = WatchlistMovieSerializer(watchlist_movies, many=True)
        return Response(serializer.data)
