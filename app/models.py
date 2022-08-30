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


RolesType = Literal["member", "moderator", "admin"]


class User(BaseModel):
    role: models.CharField[RolesType]
    posts: Manager[Post]
    threads: models.ManyToManyField[Thread, UserThread]

    email = models.EmailField(unique=True)

    ROLE_MEMBER = "member"
    ROLE_MODERATOR = "moderator"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = (
        (ROLE_MEMBER, ROLE_MEMBER),
        (ROLE_MODERATOR, ROLE_MODERATOR),
        (ROLE_ADMIN, ROLE_ADMIN),
    )
    role = models.CharField(  # type: ignore
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_MEMBER,
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"


class Post(BaseModel):
    user_id: int
    thread_id: int
    thread: models.ForeignKey[Thread]

    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    thread = models.ForeignKey("Thread", related_name="posts", on_delete=models.CASCADE)
    text = models.CharField(max_length=10000, blank=False)
    is_deleted = models.BooleanField(default=False)


class Thread(BaseModel):
    moderator_id: int | None
    posts: Manager[Post]
    users: models.ManyToManyField[User, UserThread]

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
    Send email notification to each user, with text from all posts in threads user is subscribed to.
    """
    for thread in Thread.objects.prefetch_related("users", "posts"):
        new_posts = list(thread.posts.filter(created_at__gt=timezone.now() - timedelta(days=7)))
        if not new_posts:
            continue
        for user in thread.users.all():
            send_email(user.email, "".join(post.text for post in new_posts))
