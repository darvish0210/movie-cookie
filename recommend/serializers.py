# recommend/serializers.py
from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    RelatedField,
    ValidationError,
)
from .models import Recommend
from movieinfo.models import Genre


class GenreRelatedField(RelatedField):
    # 직렬화된 형식 -> 파이썬 데이터 형식 변환
    def to_internal_value(self, data):
        try:
            genre = Genre.objects.get(genre=data)
            return genre
        except Genre.DoesNotExist:
            raise ValidationError("Invalid genre name.")

    # 파이썬 데이터 -> 직렬화된 형식 변환
    def to_representation(self, value):
        return value.genre


class RecommendSerializer(ModelSerializer):
    # movie_id: generate 요청에서는 사용X, 응답으로 받아서 객체 저장 요청 시 사용
    movie_id = IntegerField(required=False)
    genre = GenreRelatedField(queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Recommend
        fields = [
            "id",
            "user",
            "genre",
            "nation_korean",
            "nation_foreign",
            "period_2000",
            "period_2010",
            "period_2020",
            "movie_id",
            "movie_title",
            "poster_url",
            "movie",
        ]
        read_only_fields = ("user", "movie")
