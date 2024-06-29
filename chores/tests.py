from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Chore
from .forms import CreateChoreForm
from django.urls import reverse
from django.core.mail import send_mail

class ChoreModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="test_password")
        self.chore = Chore.objects.create(
            chore="Test Chore",
            assigned_date=timezone.now(),
            due_date=timezone.now() + timezone.timedelta(days=3),
            chore_assigner="Assigner",
            assign_chore_to=self.user,
        )

    def test_chore_is_expired(self):
        self.assertFalse(self.chore.is_expired())
        self.chore.due_date = timezone.now() - timezone.timedelta(days=1)
        self.chore.save()
        self.assertTrue(self.chore.is_expired())

    def test_chore_str_method(self):
        expected_str = 'Test Chore by test_user'
        self.assertEqual(str(self.chore), expected_str)

class ChoreViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="test_password")
        self.chore = Chore.objects.create(
            chore="Test Chore",
            assigned_date=timezone.now(),
            due_date=timezone.now() + timezone.timedelta(days=3),
            chore_assigner="Assigner",
            assign_chore_to=self.user,
        )

    def test_index_view(self):
        response = self.client.get(reverse('chores:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['chore_list'], ['<Chore: Test Chore by test_user>'])

    def test_create_chore_view(self):
        response = self.client.get(reverse('chores:create_chore'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username="test_user", password="test_password")
        response = self.client.get(reverse('chores:create_chore'))
        self.assertEqual(response.status_code, 200)

        form_data = {
            'chore': 'New Test Chore',
            'due_date': timezone.now() + timezone.timedelta(days=5),
            'assign_chore_to': self.user.id,
        }
        response = self.client.post(reverse('chores:create_chore'), data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['chore_list'], ['<Chore: Test Chore by test_user>', '<Chore: New Test Chore by test_user>'])

    def test_create_chore_form_validity(self):
        form_data = {
            'chore': '',
            'due_date': timezone.now() + timezone.timedelta(days=5),
            'assign_chore_to': self.user.id,
        }
        form = CreateChoreForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data['chore'] = 'Valid Chore Name'
        form = CreateChoreForm(data=form_data)
        self.assertTrue(form.is_valid())
        
def test_create_chore_email_notification(self):
    response = self.client.get(reverse('chores:create_chore'))
    self.assertEqual(response.status_code, 302)

    self.client.login(username="test_user", password="test_password")
    response = self.client.get(reverse('chores:create_chore'))
    self.assertEqual(response.status_code, 200)

    form_data = {
        'chore': 'New Test Chore',
        'due_date': timezone.now() + timezone.timedelta(days=5),
        'assign_chore_to': self.user.id,
        'send_notification': True, 
    }
    response = self.client.post(reverse('chores:create_chore'), data=form_data, follow=True)
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context['chore_list'], ['<Chore: Test Chore by test_user>', '<Chore: New Test Chore by test_user>'])

    
    sent_mail = self.get_sent_mail()
    self.assertEqual(len(sent_mail), 1)
    self.assertEqual(sent_mail[0].subject, "Household Chores Distributor")

     