from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "nickname",
            "genre",
            "bio",
            "profile_picture",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        genre_data = validated_data.pop("genre", None)
        user = User.objects.create_user(**validated_data)
        # 다 대 다 직접할당 x
        if genre_data:
            user.genre.set(genre_data)

        return user
