from rest_framework.test import APITestCase

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

        resp = self.client.post(self.register_url, data=payload)

        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        payload = {"username": "rohan", "password": "hello@123"}

        self.client.post(self.register_url, data=payload)

        resp = self.client.post(self.login_url, data=payload)
        result = resp.json()

        self.assertEqual(resp.status_code, 200)

        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    def test_refresh(self):
        payload = {"username": "rohan", "password": "hello@123"}

        self.client.post(self.register_url, data=payload)

        resp = self.client.post(self.login_url, data=payload)
        refresh = resp.json()["refresh"]

        resp = self.client.post(self.refresh_url, data={"refresh": refresh})
        result = resp.json()

        self.assertEqual(resp.status_code, 200)

        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])
