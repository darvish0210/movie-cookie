from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import MovieInfo, OneLineCritic


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
        if value < 0 or value > 5:
            raise ValidationError("잘못된 별점 입력입니다.")
        return value

    def validate_movie(self, value):
        try:
            MovieInfo.objects.get(id=value.id)
        except:
            raise ValidationError("잘못된 접근입니다.")
        return value
