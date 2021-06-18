from django.db import models


class Message(models.Model):

    sender = models.ForeignKey(
        "user_control.CustomUser",
        related_name="message_sender",
        on_delete=models.CASCADE,
    )
    reciever = models.ForeignKey(
        "user_control.CustomUser",
        related_name="message_reciever",
        on_delete=models.CASCADE,
    )
    message = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message between {self.sender.username} and {self.reciever.username}"


class MessageAttachment(models.Model):

    message = models.ForeignKey(
        Message, related_name="message_attachments", on_delete=models.CASCADE
    )
    attachment = models.FileField(upload_to="message/attachments")
    caption = models.CharField(max_length=225, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message Attachment"
        verbose_name_plural = "Message Attachments"

    def __str__(self):
        return self.message
