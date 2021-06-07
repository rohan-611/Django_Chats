from rest_framework import serializers

from .models import Message, MessageAttachment


class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        models = MessageAttachment
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField("get_user_data")
    sender_id = serializers.IntegerField(write_only=True)
    reciever = serializers.SerializerMethodField("get_user_data")
    reciever_id = serializers.IntegerField(write_only=True)
    message_attachments = MessageAttachmentSerializer(read_only=True, many=True)

    class Meta:
        models = Message
        fields = "__all__"

    def get_user_data(self, obj):
        from user_control.serializers import UserProfileSerializer

        return UserProfileSerializer(obj.sender.user_profile)
