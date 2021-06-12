from rest_framework.test import APITestCase

# Create your tests here.


class TestMessage(APITestCase):
    message_url = "/message/message"

    def setUp(self):
        from user_control.models import CustomUser, UserProfile

        self.sender = CustomUser.objects._create_user("sender", "sender123")
        UserProfile.objects.create(
            first_name="Sender",
            last_name="Sender",
            user=self.sender,
            caption="Sender",
            about="Sender",
        )
        self.reciever = CustomUser.objects._create_user("reciever", "reciever123")
        UserProfile.objects.create(
            first_name="Reciever",
            last_name="Reciever",
            user=self.reciever,
            caption="Reciever",
            about="Reciever",
        )

        self.client.force_authenticate(user=self.sender)

    def test_post_message(self):
        payload = {
            "sender_id": self.sender.id,
            "reciever_id": self.reciever.id,
            "message": "Test Message",
        }

        response = self.client.post(self.message_url, data=payload)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["message"], "Test Message")
        self.assertEqual(result["sender"]["user"]["username"], "sender")
        self.assertEqual(result["reciever"]["user"]["username"], "reciever")
