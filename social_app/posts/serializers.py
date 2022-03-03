from rest_framework import serializers
from .models import Posts
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['title', 'content']

    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     user = User.objects.create(**validated_data)
    #     Posts.objects.create(user=user, **profile_data)
    #     return user
