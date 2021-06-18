from rest_framework import serializers

from .models import Message, MessageAttachment


class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField("get_sender_data")
    sender_id = serializers.IntegerField(write_only=True)
    reciever = serializers.SerializerMethodField("get_reciever_data")
    reciever_id = serializers.IntegerField(write_only=True)
    message_attachments = MessageAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Message
        fields = "__all__"

    def get_sender_data(self, obj):
        from user_control.serializers import UserProfileSerializer

        return UserProfileSerializer(obj.sender.user_profile).data

    def get_reciever_data(self, obj):
        from user_control.serializers import UserProfileSerializer

        return UserProfileSerializer(obj.reciever.user_profile).data
