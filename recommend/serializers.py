# recommend/serializers.py
from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Recommend


class RecommendSerializer(ModelSerializer):
    # Recommend객체 생성/수정시 연결할 MovieInfo객체를 알려주는 용도 - generate에서는 사용X
    movie_id = IntegerField(required=False)

    class Meta:
        model = Recommend
        fields = [
            "user",
            "input_genre",
            "input_nation",
            "input_period",
            "movie_id",
            "movie",
        ]
        read_only_fields = ("user", "movie")
