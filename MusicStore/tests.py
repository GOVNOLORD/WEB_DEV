from django.test import TestCase
from instruments.models import CustomUser
from rest_framework.test import APIClient
from rest_framework import status
from instruments.permissions import IsAdmin
from rest_framework.test import APIRequestFactory
from instruments.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'testuser', 'password': 'testpassword'}
        self.user = User.objects.create_user(**self.user_data)

    def test_registration_endpoint(self):
        response = self.client.post('/api/registration/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_endpoint(self):
        response = self.client.post('/api/token/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class CustomPermissionTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_user(username='testuser', is_stuff=True)
        self.non_admin_user = CustomUser.objects.create(username='nonadminuser', is_stuff=False)

    def test_is_admin_permissions(self):
        request = self.factory.get('/some-endpoint')
        request.user = self.user
        permission = IsAdmin
        self.assertTrue(permission.has_permission(request, None))

    def test_non_admin_user_premission(self):
        request = self.factory.get('/some-endpoint')
        request.user = self.non_admin_user
        permission = IsAdmin()
        self.assertFalse(permission.has_permission(request, None))


class SerializerValidationTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'}

    def test_email_format_validation(self):
        invalid_email_data = {'username': 'testuser', 'email': 'invalid_email', 'password': 'testpassword'}
        serializer = UserSerializer(data=invalid_email_data)
        self.assertFalse(serializer.is_valid())

    def test_username_uniqueness_validation(self):
        user = CustomUser.objects.create_user(**self.user_data)
        duplicate_data = {'username': 'testuser', 'email': 'another@example.com', 'password': 'testpassword'}
        serializer = UserSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
