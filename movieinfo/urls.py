from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

movieInfoRouter = DefaultRouter()
movieInfoRouter.register("detail", views.MovieInfoViewSet)
oneLineCriticRouter = DefaultRouter()
oneLineCriticRouter.register("onelinecritic", views.OneLineCriticViewSet)

urlpatterns = [
    path("search/", views.SerachMovieAPIView.as_view(), name="search"),
    path("", include(movieInfoRouter.urls)),
    path("detail/<int:movie_id>/", include(oneLineCriticRouter.urls)),
]
