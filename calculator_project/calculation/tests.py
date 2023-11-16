from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Calculation


class EvaluationTestCase(APITestCase):

    def test_empty_expression(self):
        data = {"expression": ""}
        response = self.client.post(reverse('evaluate_expression'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No expression provided', response.data['error'])

    def test_division_by_zero(self):
        data = {"expression": "1 / 0"}
        response = self.client.post(reverse('evaluate_expression'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Division by zero', response.data['error'])

    def test_invalid_expression(self):
        data = {"expression": "2 + "}
        response = self.client.post(reverse('evaluate_expression'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid expression', response.data['error'])

    def test_disallowed_expression_component(self):
        data = {"expression": "1 + math.sqrt(4)"}
        response = self.client.post(reverse('evaluate_expression'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Disallowed expression component', response.data['error'])


class HistoryTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        Calculation.objects.create(user=self.user, expression='1 + 1', result=2)
        Calculation.objects.create(user=self.user, expression='2 + 2', result=4)

    def test_history_unauthenticated(self):
        response = self.client.get(reverse('calculation_history'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_history_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('calculation_history'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming 2 calculations were made
