from rest_framework import viewsets, status
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


class PostLikeDislikeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for posts like dislike model.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostLikeDislikeSerializer
    queryset = PostLikeDislike.objects.all()

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
