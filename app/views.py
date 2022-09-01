from __future__ import annotations

from django.db.models.query import QuerySet
from django.http.response import Http404
from rest_framework import generics, permissions
from rest_framework.request import Request


class UserPostListCreate(generics.ListAPIView):
    # request: UserRequest
    permission_classes = (permissions.IsAuthenticated,)
    # serializer_class = ...

    def get_queryset(self):
        """
        List authenticated user's posts.
        """

    def perform_create(self, serializer):
        """
        Create post authored by authenticated user.
        """


class PostRetrieveUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    # serializer_class = ...

    def get_queryset(self):
        return Post.objects.all()

    def perform_update(self, serializer):
        """
        Member can update their own posts, moderator can update any posts in thread they moderate, admin can update any
        post.
        """
        super().perform_update(serializer)


class ThreadSubscribe(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Thread.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Add user to thread.
        """


class ThreadUnsubscribe(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Thread.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Remove user from thread.
        """
