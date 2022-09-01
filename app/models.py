from __future__ import annotations

from datetime import timedelta
from typing import Any, Literal

from django.db import models
from django.db.models.manager import Manager
from django.utils import timezone


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):

    email = models.EmailField(unique=True)

    ROLE_MEMBER = "member"
    ROLE_MODERATOR = "moderator"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = (
        (ROLE_MEMBER, ROLE_MEMBER),
        (ROLE_MODERATOR, ROLE_MODERATOR),
        (ROLE_ADMIN, ROLE_ADMIN),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_MEMBER,
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"


class Post(BaseModel):

    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    thread = models.ForeignKey("Thread", related_name="posts", on_delete=models.CASCADE)
    text = models.CharField(max_length=10000, blank=False)
    is_deleted = models.BooleanField(default=False)


class Thread(BaseModel):

    moderator = models.ForeignKey(User, related_name="threads", null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=10000, blank=False)
    users = models.ManyToManyField(
        User,
        related_name="users",
        blank=True,
        through="UserThread",
    )


class UserThread(BaseModel):
    user = models.ForeignKey(User, related_name="user_threads", on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, related_name="user_threads", on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)


def send_email(email, text):
    pass


def send_notifications():
    """
    Send email notification to each user, with text from all posts in threads user is subscribed to, in last 7 days.
    """
