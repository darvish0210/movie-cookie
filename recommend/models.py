# recommend/models.py
from django.db import models
from movieinfo.models import MovieInfo
from django.contrib.auth.models import User


class Recommend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommends")
    # 유저 구현 후 'accounts.User'로 바꾸기

    input_nation = models.CharField(max_length=5)
    input_period = models.CharField(max_length=14)
    input_genre = models.TextField()

    movie = models.ForeignKey(
        MovieInfo, on_delete=models.CASCADE, related_name="recommends"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return f"{self.id}: {self.user} - {self.movie}"
