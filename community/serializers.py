from rest_framework import serializers
from .models import Post, Comment


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
            "content",
            "image",
            "created_at",
            "updated_at",
            "view_count",
            "comments",
        ]
        # read_only_fields = ["user"]

    # def get_user_name(self, obj):
    #     return obj.user.user_name

    # def create(self, validated_data):

    #     validated_data["user"] = self.context["request"].user
    #     return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    # author_username = serializers.SerializerMethodField()
    reply = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            # "user",
            # "user_name",
            "content",
            "created_at",
            "updated_at",
            "parent",
            "reply",
        ]
        # read_only_fields = ["user"]

    # def get_user_name(self, obj):
    #     return obj.user.user_name

    # def create(self, validated_data):
    #     validated_data["user"] = self.context["request"].user
    #     return super().create(validated_data)
    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind("", self)
        return serializer.data


class PostOnlySerializer(serializers.ModelSerializer):
    parent_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "parent_comments")

    def get_parent_comments(self, obj):
        parent_comments = obj.comments.filter(parent=None)
        serializer = CommentSerializer(parent_comments, many=True)
        return serializer.data
