from django.contrib.auth import get_user_model, authenticate, login

from accounts.models import User

from django.core.signing import Signer
from django.test import Client
from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user_1',
            'password1': '123qwe!@#',
            'password2': '123qwe!@#',
            'email': 'user_1@test.com'
        }
        self.client = Client()
        self.registration_url = reverse('accounts:register')
        self.registration_done_url = reverse('accounts:register_done')

    def test_registration_valid(self):
        response = self.client.post(self.registration_url, self.data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.registration_done_url, status_code=302, target_status_code=200)
        self.assertEqual(response.url, self.registration_done_url)

        user = User.objects.first()
        self.assertEqual(user.username, self.data['username'])
        self.assertEqual(user.email, self.data['email'])
        self.assertTrue(user.check_password(self.data['password1']))
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_activated)

    def test_registration_invalid(self):
        self.data['password2'] = '123qwe!@'

        response = self.client.post(self.registration_url, self.data)
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(response.context['form'].is_valid())
        user = User.objects.filter(username=self.data['username'])
        self.assertEqual(len(user), 0)

    def test_activation_url(self):
        response = self.client.post(self.registration_url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.registration_done_url, status_code=302, target_status_code=200)

        user = User.objects.first()
        self.assertEqual(user.username, self.data['username'])

        signer = Signer()
        response = self.client.get(
            'http://localhost' + reverse('accounts:register_activate', kwargs={'sign': signer.sign(user.username)})
        )
        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_activated)

    def test_page_not_found(self):
        response = self.client.get('/non-existing-page')
        self.assertEqual(response.status_code, 404)


class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.user_reactivate_url = reverse("accounts:reactivation")
        self.username = 'user_1'
        self.password = '123qwe!@#'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_success(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'), status_code=302, target_status_code=200)
        user = authenticate(username=self.username, password=self.password)
        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)

    def test_login_failure(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 200)
        user = authenticate(username=self.username, password='wrong_password')
        self.assertIsNone(user)
