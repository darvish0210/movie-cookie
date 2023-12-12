from django.urls import path, include
from . import views


urlpatterns = [path("search/", views.SerachMovieInDB.as_view(), name="search")]
