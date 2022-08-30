from __future__ import annotations

from django.db.models.query import QuerySet
from django.http.response import Http404
from rest_framework import generics, permissions
from rest_framework.request import Request

from app.models import User, Post, Thread


class UserRequest(Request):
    user: User


class UserPostListCreate(generics.ListAPIView):
    request: UserRequest
    permission_classes = (permissions.IsAuthenticated,)
    # serializer_class = ...

    def get_queryset(self) -> QuerySet[Post]:
        """
        List authenticated user's posts.
        """
        return Post.objects.filter(user_id=self.request.user.id).order_by("-created_at")

    def perform_create(self, serializer):
        """
        Create post authored by authenticated user.
        """
        serializer.save(user=self.request.user)


class PostRetrieveUpdate(generics.RetrieveUpdateAPIView):
    request: UserRequest
    permission_classes = (permissions.IsAuthenticated,)
    # serializer_class = ...

    def get_queryset(self):
        return Post.objects.all()

    def perform_update(self, serializer):
        """
        Member can update their own posts, moderator can update any posts in thread they moderate, admin can update any
        post.
        """
        post: Post = self.get_object()
        user = self.request.user

        if user.role == "member":
            if post.user_id != user.id:
                raise Http404

        elif user.role == "moderator":
            if post.user_id != user.id and post.thread.moderator != user:
                raise Http404

        super().perform_update(serializer)


class ThreadSubscribe(generics.GenericAPIView):
    request: UserRequest
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Thread.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Add user to thread.
        """
        thread: Thread = self.get_object()
        thread.users.add(self.request.user)


class ThreadUnsubscribe(generics.GenericAPIView):
    request: UserRequest
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Thread.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Remove user from thread.
        """
        thread: Thread = self.get_object()
        thread.users.remove(self.request.user)
