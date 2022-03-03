from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import Posts
from .serializers import PostSerializer


class PostViewSet(viewsets.ViewSet):
    """
    ViewSet for posts model.
    """
    serializer_class = PostSerializer
    queryset = Posts.objects.all()

    def retrieve(self, request, pk=None):
        queryset = Posts.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def list(self, request):
        queryset = Posts.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        title = request.data.get("title", "")
        content = request.data.get("content", "")
        new_post = {}

        if title != "" and content != "":
            new_post, _created = Posts.objects.get_or_create(user=request.user, title=title, content=content)

        serializer = PostSerializer(new_post)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = Posts.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        if post:
            title = request.data.get("title", "")
            content = request.data.get("content", "")
            if title != "" and content != "":
                post.title = title
                post.content = content
                post.save()

        serializer = PostSerializer(post)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Posts.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        if post:
            post.delete()

        return Response({"message": "Post with pk-{} has been removed!".format(pk)})
