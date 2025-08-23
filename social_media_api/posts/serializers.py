from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class CommentSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at", "updated_at"]
        read_only_fields = ["author", "created_at", "updated_at"]


class PostSerializer(serializers.ModelSerializer):
    author = UserMiniSerializer(read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
            "comments_count",
        ]
        read_only_fields = ["author", "created_at", "updated_at", "comments_count"]