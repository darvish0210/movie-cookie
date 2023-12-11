from django.urls import path, include
from .getdatas import getMovieInfo

urlpatterns = [
    path('test/', getMovieInfo)
]
