from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class AuthTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/auth/register/"
        self.token_url = "/api/auth/token/"
        self.profile_url = "/api/auth/profile/"

    def test_user_registration(self):
        response = self.client.post(self.register_url, {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        User.objects.create_user(username="testuser", password="testpass123")
        response = self.client.post(self.token_url, {
            "username": "testuser",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_login(self):
        response = self.client.post(self.token_url, {
            "username": "wrong",
            "password": "wrong"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_requires_auth(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_accessible_with_auth(self):
        from authentication.models import Profile
        user = User.objects.create_user(username="testuser", password="testpass123")
        Profile.objects.create(user=user)
        token_response = self.client.post(self.token_url, {
            "username": "testuser",
            "password": "testpass123"
        })
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
