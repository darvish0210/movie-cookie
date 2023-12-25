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
    """
    `Recommend`모델과 다대다 관계로 연결 된 `Genre`모델을 `RecommendSerializer`에서 처리하기 위한 필드입니다.
    """

    def to_internal_value(self, data):
        """
        `JSON`으로 직렬화된 데이터를 받아, `Genre`객체로 변환합니다.
        """
        try:
            genre = Genre.objects.get(genre=data)
            return genre
        except Genre.DoesNotExist:
            raise ValidationError("Invalid genre name.")

    def to_representation(self, value):
        """
        `Genre`객체에서 `JSON`으로 직렬화합니다.
        """
        return value.genre


class RecommendSerializer(ModelSerializer):
    """
    이 시리얼라이저는 `Recommend` 객체를 직렬화하는 역할을 합니다.\n
    `movie_id`는 `generate` 요청에서는 사용하지 않고, `generate`의 응답으로 받아서 `Recommend` 객체 저장 요청 시 사용합니다.
    """

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
            "created_at",
        ]
        read_only_fields = ("user", "movie")
