from django.db import models


class MovieInfo(models.Model):
    id = models.AutoField(primary_key=True)
    searchTitle = models.TextField()
    title = models.TextField()
    posters = models.TextField(blank=True, null=True)
    vods = models.TextField(blank=True, null=True)
    directors = models.TextField(blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    nations = models.TextField(blank=True, null=True)
    companies = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    rating = models.TextField(blank=True, null=True)
    genres = models.ManyToManyField(
        "Genre", related_name="movieinfo", blank=True, null=True
    )
    releaseDate = models.DateField(blank=True, null=True)


class OneLineCritic(models.Model):
    id = models.AutoField(primary_key=True)
    # author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
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


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=16, unique=True)
    slug = models.SlugField(
        max_length=200, db_index=True, unique=True, allow_unicode=True
    )

    def __str__(self):
        return self.genre

    def get_absolute_url(self):
        return f"/movieinfo/genre/{self.slug}"


class TestLikeMovie(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey("MovieInfo", on_delete=models.CASCADE)


class TestWatchedMovie(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey("MovieInfo", on_delete=models.CASCADE)


class TestWatchlistMovie(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey("MovieInfo", on_delete=models.CASCADE)
