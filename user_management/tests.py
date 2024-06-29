from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import ExtendedUserCreationForm
from .views import SignUp

class ExtendedUserCreationFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = ExtendedUserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_missing_email(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = ExtendedUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_invalid_email(self):
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = ExtendedUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_password_mismatch(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'mismatchedpassword',
        }
        form = ExtendedUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

class SignUpViewTest(TestCase):
    def test_signup_view(self):
        response = self.client.get(reverse('user_management:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_management/signup.html')
        self.assertIsInstance(response.context['form'], ExtendedUserCreationForm)

    def test_signup_form_submission(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('user_management:signup'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup_form_with_invalid_data(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'mismatchedpassword',
        }
        response = self.client.post(reverse('user_management:signup'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())

