from django.urls import path
from .views import obtain_jwt_token

urlpatterns = [
    path("token/", obtain_jwt_token, name="obtain_token"),
]
