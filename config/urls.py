from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("movieinfo/", include("movieinfo.urls")),
    path("recommend/", include("recommend.urls")),
]
