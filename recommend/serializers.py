# recommend/serializers.py
from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Recommend
from movieinfo.models import MovieInfo


class RecommendSerializer(ModelSerializer):
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
