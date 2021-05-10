from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Message(models.Model):

    author = models.ForeignKey(
        User, related_name="author_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.author.username
