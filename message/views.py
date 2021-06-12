from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import Message, MessageAttachment, MessageSerializer

# Create your views here.


class MessageView(ModelViewSet):
    queryset = Message.objects.select_related("sender", "reciever").prefetch_related(
        "message_attachments"
    )
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        request.data._mutable = True
        attachments = request.data.pop("attachments", None)

        if str(request.user.id) != str(request.data.get("sender_id", None)):
            raise Exception("Only sender can create a message")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if attachments:
            MessageAttachment.objects.bulk_create(
                [
                    MessageAttachment(**attachment, message_id=serializer.data["id"])
                    for attachment in attachments
                ]
            )

            message_data = self.get_queryset().get(id=serializer.data["id"])

            return Response(self.serializer_class(message_data).data, status=201)

        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):

        attachments = request.data.pop("attachments", None)
        instance = self.get_object()

        serializer = self.serializer_class(
            data=request.data, instance=instance, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        MessageAttachment.objects.filter(message_id=instance.id).delete()

        if attachments:
            MessageAttachment.objects.bulk_create(
                [
                    MessageAttachment(**attachment, message_id=instance.id)
                    for attachment in attachments
                ]
            )

            message_data = self.get_object()

            return Response(self.serializer_class(message_data).data, status=201)

        return Response(serializer.data, status=200)
