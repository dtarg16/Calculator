from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "testuser", "password": "somepassword", "email": "test@example.com"}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="somepassword")

    def test_login(self):
        data = {"username": "testuser", "password": "somepassword"}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)


class LogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="somepassword")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_logout(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserInformationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="somepassword", email="test@example.com")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_information(self):
        response = self.client.get(reverse('user_info'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
