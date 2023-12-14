from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import (
    MovieInfo,
    OneLineCritic,
    TestLikeMovie,
    TestWatchedMovie,
    TestWatchlistMovie,
)


class MovieInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = MovieInfo
        fields = "__all__"


class OneLineCriticSerializers(serializers.ModelSerializer):
    class Meta:
        model = OneLineCritic
        fields = "__all__"


class OneLineCriticCreateUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = OneLineCritic
        fields = ["content", "starpoint"]

    def validate_content(self, value):
        if len(value) <= 3:
            raise ValidationError("내용이 너무 짧습니다.")
        return value

    def validate_starpoint(self, value):
        if not value:
            raise ValidationError("별점을 입력하지 않았습니다.")

        if value < 0 or value > 5:
            raise ValidationError("잘못된 별점 입력입니다.")
        return value

    def validate_movie(self, value):
        try:
            MovieInfo.objects.get(id=value.id)
        except:
            raise ValidationError("잘못된 접근입니다.")
        return value


class TestLikeMovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = TestLikeMovie
        fields = ["id"]

    def validate(self, value):
        try:
            print(self._kwargs["data"]["movie_id"])
            a = TestLikeMovie.objects.get(movie=MovieInfo.objects.get(id=1))
            print(a)
        except:
            return value
        raise ValidationError("이미 좋아요를 눌렀습니다.")


class TestWatchedMovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = TestWatchedMovie
        fields = ["id"]

    def validate(self, value):
        try:
            print(self._kwargs["data"]["movie_id"])
            a = TestWatchedMovie.objects.get(movie=MovieInfo.objects.get(id=1))
            print(a)
        except:
            return value
        raise ValidationError("이미 등록되어 있습니다.")


class TestWahtchlistMovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = TestWatchlistMovie
        fields = ["id"]

    def validate(self, value):
        try:
            print(self._kwargs["data"]["movie_id"])
            a = TestWatchlistMovie.objects.get(movie=MovieInfo.objects.get(id=1))
            print(a)
        except:
            return value
        raise ValidationError("이미 등록되어 있습니다.")
