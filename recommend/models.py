# recommend/models.py
from django.db import models


class Recommend(models.Model):
    # 추천받은 유저
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="recommends"
    )

    # input 값들
    genre = models.ManyToManyField("movieinfo.Genre", related_name="recommends")
    nation_korean = models.BooleanField(default=False)
    nation_foreign = models.BooleanField(default=False)
    period_2000 = models.BooleanField(default=False)
    period_2010 = models.BooleanField(default=False)
    period_2020 = models.BooleanField(default=False)

    # 추천된 영화
    movie = models.ForeignKey(
        "movieinfo.MovieInfo", on_delete=models.CASCADE, related_name="recommends"
    )
    movie_title = models.TextField()
    poster_url = models.URLField(max_length=400, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return f"{self.id}: {self.user} - {self.movie.title}"
