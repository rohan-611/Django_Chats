from rest_framework.test import APITestCase

from .models import CustomUser
from .views import get_random, get_refresh_token, get_access_token

# Create your tests here.


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

        payload = {
            "user_id": self.user.id,
            "first_name": "Rohan",
            "last_name": "Raghuwanshi",
            "caption": "Being alive is different from living",
            "about": "I am a Developer whose also a designer",
        }

        response = self.client.post(self.profile_url, data=payload)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "Rohan")
        self.assertEqual(result["last_name"], "Raghuwanshi")
        self.assertEqual(result["user"]["username"], "rohan")
