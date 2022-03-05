from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Posts, PostLikeDislike
from .serializers import PostSerializer, PostLikeDislikeSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for posts model.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Posts.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        post_like_dislike_obj = PostLikeDislike.objects.filter(user_id=request.user.id, post_id=instance.id)
        my_post_likes = post_like_dislike_obj.filter(likes=True).count()
        my_post_dislikes = post_like_dislike_obj.filter(dislikes=True).count()

        serializer = self.get_serializer(instance)
        resp = serializer.data
        resp["likes"] = my_post_likes
        resp["dislikes"] = my_post_dislikes
        return Response(resp)

        # queryset = Posts.objects.all().select_related()
        # post = get_object_or_404(queryset, pk=1)
        # serializer = PostSerializer(post)
        # return Response(serializer.data)
    #
    # def list(self, request):
    #     post_list = list(PostLikeDislike.objects.all().select_related())
    #     print(post_list)
    #     queryset = Posts.objects.all().select_related()
    #     serializer = PostSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def create(self, request):
    #     title = request.data.get("title", "")
    #     content = request.data.get("content", "")
    #     new_post = {}
    #
    #     if title != "" and content != "":
    #         new_post, _created = Posts.objects.get_or_create(user=request.user, title=title, content=content)
    #
    #     serializer = PostSerializer(new_post)
    #     return Response(serializer.data)
    #
    # def update(self, request, pk=None):
    #     queryset = Posts.objects.all()
    #     post = get_object_or_404(queryset, pk=pk)
    #     if post:
    #         title = request.data.get("title", "")
    #         content = request.data.get("content", "")
    #         if title != "" and content != "":
    #             post.title = title
    #             post.content = content
    #             post.save()
    #
    #     serializer = PostSerializer(post)
    #     return Response(serializer.data)
    #
    # def destroy(self, request, pk=None):
    #     queryset = Posts.objects.all()
    #     post = get_object_or_404(queryset, pk=pk)
    #     if post:
    #         post.delete()
    #
    #     return Response({"message": "Post with pk-{} has been removed!".format(pk)})


class PostLikeDislikeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for posts like dislike model.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostLikeDislikeSerializer
    queryset = PostLikeDislike.objects.all()

    # def retrieve(self, request, pk=None):
    #     queryset = PostLikeDislike.objects.all()
    #     like_dislike = get_object_or_404(queryset, pk=pk)
    #     serializer = PostLikeDislikeSerializer(like_dislike)
    #     return Response(serializer.data)
    #
    # def list(self, request):
    #     print("==========")
    #     queryset = PostLikeDislike.objects.all()
    #     serializer = PostLikeDislikeSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    def create(self, request, *args, **kwargs):
        post_id = request.data.get("post", None)
        likes = request.data.get("likes", False)
        dislikes = request.data.get("dislikes", False)

        post_exist = Posts.objects.filter(id=post_id, user_id=request.user.id)
        if not post_exist:
            return Response({"success": False, "message": "Invalid Post ID"})

        if likes is False or dislikes is False:
            return Response({"success": False, "message": "Like or Dislike is required!"})

        post_action = PostLikeDislike.objects.filter(user_id=request.user.id, post_id=post_id).first()
        if post_action:
            post_action.likes = likes
            post_action.dislikes = dislikes
            post_action.save()

        else:
            post_action, _created = PostLikeDislike.objects.get_or_create(user=request.user,
                                                                          post=post_exist.first(),
                                                                          likes=likes, dislikes=dislikes)

        serializer = PostLikeDislikeSerializer(post_action)

        content = {
            "data": serializer.data,
            "message": "Post Liked / Disliked Successfully."
        }
        return Response(content, status=status.HTTP_201_CREATED)

    # def update(self, request, pk=None):
    #     queryset = Posts.objects.all()
    #     post = get_object_or_404(queryset, pk=pk)
    #     if post:
    #         title = request.data.get("title", "")
    #         content = request.data.get("content", "")
    #         if title != "" and content != "":
    #             post.title = title
    #             post.content = content
    #             post.save()
    #
    #     serializer = PostSerializer(post)
    #     return Response(serializer.data)
    #
    # def destroy(self, request, pk=None):
    #     queryset = Posts.objects.all()
    #     post = get_object_or_404(queryset, pk=pk)
    #     if post:
    #         post.delete()
    #
    #     return Response({"message": "Post with pk-{} has been removed!".format(pk)})
