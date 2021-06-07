import json
from six import BytesIO
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase

from .models import CustomUser
from .views import get_random, get_refresh_token, get_access_token


def create_image(
    storage, filename, size=(100, 100), image_mode="RGB", image_format="PNG"
):
    img_file = BytesIO()
    Image.new(image_mode, size).save(img_file, image_format)
    img_file.name = filename
    img_file.seek(0)
    return img_file


class TestGenericFunctions(APITestCase):
    def test_get_random(self):

        rand1 = get_random(10)
        rand2 = get_random(10)
        rand3 = get_random(15)

        self.assertTrue(rand1)

        self.assertNotEqual(rand1, rand2)

        self.assertEqual(len(rand1), 10)
        self.assertEqual(len(rand3), 15)

    def test_get_access_token(self):

        payload = {"id": 1}

        token = get_access_token(payload)

        self.assertTrue(token)

    def test_get_refresh_token(self):

        token = get_refresh_token()

        self.assertTrue(token)


class TestAuth(APITestCase):
    login_url = "/user/login"
    register_url = "/user/register"
    refresh_url = "/user/refresh"

    def test_register(self):
        payload = {"username": "rohan", "password": "hello@123"}

        response = self.client.post(self.register_url, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_login(self):
        payload = {"username": "rohan", "password": "hello@123"}

        self.client.post(self.register_url, data=payload)

        response = self.client.post(self.login_url, data=payload)
        result = response.json()

        self.assertEqual(response.status_code, 200)

        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    def test_refresh(self):
        payload = {"username": "rohan", "password": "hello@123"}

        self.client.post(self.register_url, data=payload)

        response = self.client.post(self.login_url, data=payload)
        refresh = response.json()["refresh"]

        response = self.client.post(self.refresh_url, data={"refresh": refresh})
        result = response.json()

        self.assertEqual(response.status_code, 200)

        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])


class TestUserInfo(APITestCase):
    profile_url = "/user/profile"

    def setUp(self):
        self.user = CustomUser.objects.create(username="rohan", password="rohan@123")
        self.client.force_authenticate(user=self.user)

    def test_post_user_profile(self):

        profile_picture = create_image(None, "profile_picture.png")

        payload = {
            "user_id": self.user.id,
            "first_name": "Rohan",
            "last_name": "Raghuwanshi",
            "caption": "Being alive is different from living",
            "about": "I am a Developer whose also a designer",
            "profile_picture": profile_picture,
        }

        response = self.client.post(self.profile_url, data=payload, format="multipart")
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "Rohan")
        self.assertEqual(result["last_name"], "Raghuwanshi")
        self.assertEqual(result["user"]["username"], "rohan")

    def test_update_user_profile(self):

        profile_picture = create_image(None, "profile_picture.png")

        payload = {
            "user_id": self.user.id,
            "first_name": "Rohan",
            "last_name": "Raghuwanshi",
            "caption": "Being alive is different from living",
            "about": "I am a Developer whose also a designer",
            "profile_picture": profile_picture,
        }

        response = self.client.post(self.profile_url, data=payload)
        result = response.json()

        # Profile Created
        # Now let's update it

        profile_picture2 = create_image(None, "profile_picture2.png")

        payload = {
            "first_name": "Ron",
            "last_name": "Ron",
            "profile_picture": profile_picture2,
        }

        response = self.client.patch(
            self.profile_url + f"/{result['id']}", data=payload
        )
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["first_name"], "Ron")
        self.assertEqual(result["last_name"], "Ron")
