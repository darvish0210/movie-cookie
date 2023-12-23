from django.db import models
from django.contrib.auth.models import AbstractUser
from movieinfo.models import Genre, MovieInfo


class User(AbstractUser):
    nickname = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    bio = models.TextField(blank=True)


class LikeMovie(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(MovieInfo, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")


class WatchedMovie(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(
        MovieInfo, on_delete=models.CASCADE, related_name="watcheds"
    )
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="watcheds")


class WatchlistMovie(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(
        MovieInfo, on_delete=models.CASCADE, related_name="watchlists"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="watchlists"
    )
