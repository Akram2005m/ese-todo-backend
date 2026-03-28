from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from todo.models import Todo


class TodoTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        token_response = self.client.post("/api/auth/token/", {
            "username": "testuser",
            "password": "testpass123"
        })
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.todos_url = "/api/todos/"

    def test_create_todo(self):
        response = self.client.post(self.todos_url, {
            "title": "Test Todo",
            "description": "Test description",
            "priority": "medium"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test Todo")

    def test_list_todos(self):
        Todo.objects.create(user=self.user, title="Todo 1")
        Todo.objects.create(user=self.user, title="Todo 2")
        response = self.client.get(self.todos_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_todo(self):
        todo = Todo.objects.create(user=self.user, title="Old Title")
        response = self.client.patch(f"{self.todos_url}{todo.id}/", {
            "title": "New Title"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New Title")

    def test_delete_todo(self):
        todo = Todo.objects.create(user=self.user, title="To Delete")
        response = self.client.delete(f"{self.todos_url}{todo.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_todo_requires_auth(self):
        self.client.credentials()
        response = self.client.get(self.todos_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_see_other_users_todos(self):
        other_user = User.objects.create_user(username="other", password="otherpass123")
        Todo.objects.create(user=other_user, title="Other Todo")
        response = self.client.get(self.todos_url)
        self.assertEqual(len(response.data), 0)
