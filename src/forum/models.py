from random import choice

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE, SET_DEFAULT
from django.utils.translation import gettext_lazy as _
from faker import Faker

from common.models import BaseModel

# Create your models here.


class Conversation(BaseModel):
    title = models.CharField(max_length=100, help_text=_("The maximum number of characters is 100."))
    author = models.ForeignKey(get_user_model(), on_delete=CASCADE)
    content = models.TextField(
        blank=True,
        max_length=5000,
        help_text=_("The maximum number of characters is 5000."),
    )
    image = models.ImageField(upload_to="forum/conversation/images", null=True, blank=True)

    def __str__(self):
        return f"({self.pk}){self.author.username if self.author else 'Unknown'} created: {self.created_at} last updated: {self.last_updated}"

    @classmethod
    def generate_conversations(cls, count):
        conversations = []
        faker = Faker()
        users = get_user_model().objects.all()
        for i in range(count):
            user = choice(users)
            conversation = Conversation(
                title=faker.text(max_nb_chars=100),
                author=user,
                content=faker.text(max_nb_chars=4999),
            )
            conversations.append(conversation)
        Conversation.objects.bulk_create(conversations)


class Comments(BaseModel):
    author = models.ForeignKey(get_user_model(), on_delete=CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(
        blank=True,
        max_length=2000,
        help_text=_("The maximum number of characters is 2000."),
    )
    image = models.ImageField(upload_to="forum/comments/images", null=True, blank=True)

    def __str__(self):
        return f"{self.author.username if self.author else 'Unknown'} commented: {self.created_at} last updated: {self.last_updated}"

    @classmethod
    def generate_comments(cls, count):
        comments = []
        faker = Faker()
        conversations = Conversation.objects.all()
        users = get_user_model().objects.all()
        for i in range(count):
            conversation = choice(conversations)
            user = choice(users)
            comment = Comments(
                author=user,
                conversation=conversation,
                content=faker.text(max_nb_chars=2000),
            )
            comments.append(comment)
        Comments.objects.bulk_create(comments)
