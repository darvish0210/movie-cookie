# recommend/serializers.py
from rest_framework.serializers import ModelSerializer
from .models import Recommend


class RecommendSerializer(ModelSerializer):
    class Meta:
        model = Recommend
        fields = ["user", "input_genre", "input_nation", "input_period", "movie"]
        read_only_fields = ("user",)
