from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    # user_name = serializers.SerializerMethodField()

    # comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = [
            "id",
            # "user",
            # "user_name",
            "title",
            "context",
            "image",
            "created_at",
            "updated_at",
            "view_count",
            # "comments",
        ]
        # read_only_fields = ["user"]

    # def get_user_name(self, obj):
    #     return obj.user.user_name

    # def create(self, validated_data):

    #     validated_data["user"] = self.context["request"].user
    #     return super().create(validated_data)
