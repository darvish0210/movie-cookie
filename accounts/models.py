from django.db import models
from django.contrib.auth.models import AbstractUser
from movieinfo.models import Genre


class User(AbstractUser):
    nickname = models.CharField(max_length=255)
    ganre = models.ManyToManyField(Genre, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    bio = models.TextField(blank=True)
