from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserCreateView,
    UserProfileViewSet,
    LikedMoviesView,
    WatchedMoviesView,
    WatchlistMoviesView,
)

router = DefaultRouter()
router.register(r"user-profile", UserProfileViewSet, basename="user-profile")

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("signup/", UserCreateView.as_view(), name="signup"),
    path("api/", include(router.urls)),
    path("api/liked-movies/", LikedMoviesView.as_view(), name="liked-movies"),
    path("api/watched-movies/", WatchedMoviesView.as_view(), name="watched-movies"),
    path(
        "api/watchlist-movies/", WatchlistMoviesView.as_view(), name="watchlist-movies"
    ),
]
