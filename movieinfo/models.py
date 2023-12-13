from django.db import models


class MovieInfo(models.Model):
    id = models.AutoField(primary_key=True)
    searchTitle = models.TextField()
    title = models.TextField()
    posters = models.TextField(blank=True, null=True)
    vods = models.TextField(blank=True, null=True)
    directors = models.CharField(max_length=64, blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    nations = models.CharField(max_length=64, blank=True, null=True)
    companies = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    rating = models.CharField(max_length=64, blank=True, null=True)
    genres = models.CharField(max_length=64, blank=True, null=True)
    releaseDate = models.DateField(blank=True, null=True)


class OneLineCritic(models.Model):
    id = models.AutoField(primary_key=True)
    # author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    movie = models.ForeignKey("MovieInfo", on_delete=models.CASCADE)
    content = models.TextField()
    starpoint = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
