from django.db import models


class MovieInfo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    poster = models.URLField(blank=True, null=True)
    director = models.CharField(max_length=64, blank=True, null=True)
    actor = models.CharField(max_length=64, blank=True, null=True)
    nation = models.CharField(max_length=64, blank=True, null=True)
    company = models.CharField(max_length=64, blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=64, blank=True, null=True)
    releaseDate = models.DateField(blank=True, null=True)


class OneLineCritic(models.Model):
    id = models.AutoField(primary_key=True)
    # author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    movie = models.ForeignKey("MovieInfo", on_delete=models.CASCADE)
    content = models.TextField()
    starpoint = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
