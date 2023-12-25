from django.db import models
from django.utils.text import slugify


class MovieInfo(models.Model):
    id = models.AutoField(primary_key=True)
    searchTitle = models.TextField()
    docid = models.CharField(max_length=16, unique=True)
    title = models.TextField()
    posters = models.ManyToManyField("Poster", blank=True, related_name="movieinfo")
    vods = models.ManyToManyField("Vod", blank=True, related_name="movieinfo")
    directors = models.ManyToManyField("Director", blank=True, related_name="movieinfo")
    actors = models.ManyToManyField("Actor", blank=True, related_name="movieinfo")
    nations = models.ManyToManyField("Nation", blank=True, related_name="movieinfo")
    companies = models.ManyToManyField("Company", blank=True, related_name="movieinfo")
    plot = models.TextField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    rating = models.TextField(blank=True, null=True)
    genres = models.ManyToManyField("Genre", blank=True, related_name="movieinfo")
    release_date = models.DateField(blank=True, null=True)


class OneLineCritic(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    movie = models.ForeignKey("MovieInfo", on_delete=models.CASCADE)
    content = models.TextField()
    starpoint = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GPTAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.OneToOneField("MovieInfo", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    num_of_critics = models.IntegerField(blank=True, null=True)


class Poster(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.TextField()


class Vod(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    url = models.TextField()


class Actor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    number = models.IntegerField(unique=True)


class Director(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    number = models.IntegerField(unique=True)


class Nation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=16, unique=True)
    slug = models.SlugField(
        max_length=200, db_index=True, unique=True, allow_unicode=True
    )

    def save(self, **kwargs):
        self.slug = slugify(self.genre, allow_unicode=True)
        super(Genre, self).save(**kwargs)

    def __str__(self):
        return self.genre

    def get_absolute_url(self):
        return f"/movieinfo/genre/{self.slug}"
