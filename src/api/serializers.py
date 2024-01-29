from rest_framework import serializers
from user.models import Profile
from feed.models import Post, Like, Comment
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "profile_image",
            "bio",
            "email",
            "posts_count",
            "follower_count",
            "following_count",
        ]

    def get_posts_count(self, obj):
        return obj.get_posts_count()

    def get_follower_count(self, obj):
        return obj.get_follower_count

    def get_following_count(self, obj):
        return obj.get_following_count


class LikeSerilizer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment"]


class PostSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "image",
            "caption",
            "location",
            "comment",
            "get_like_count",
        ]

    def get_like_count(self, obj):
        return obj.get_like_count

    def get_comment(self, obj):
        comment = obj.comment_set.all()
        serializer = CommentSerializer(comment, many=True)
        return serializer.data
