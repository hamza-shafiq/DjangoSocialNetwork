from rest_framework import serializers
from .models import Posts, PostLikeDislike


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = "__all__"


class PostLikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikeDislike
        fields = "__all__"
