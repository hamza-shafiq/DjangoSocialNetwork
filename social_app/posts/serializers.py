from rest_framework import serializers
from .models import Posts, PostLikeDislike
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = "__all__"

    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     user = User.objects.create(**validated_data)
    #     Posts.objects.create(user=user, **profile_data)
    #     return user


class PostLikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikeDislike
        fields = "__all__"
