from django.test import TestCase
from django.urls import reverse
from .accounts import create_one_account


class PageTestCase(TestCase):

    def test_front_page_200(self):
        # frontpage
        response = self.client.get(reverse('front_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in with Github')

    def test_non_login_settings_404(self):
        response = self.client.get(reverse('settings'))
        self.assertContains(response, 'Please login to see this page.')

    def test_user_login_frontpage_settings(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(reverse('front_page'))
        self.assertNotContains(response, 'Log in with Github')
        self.assertContains(response, 'Find a Job')
        response = self.client.get(reverse('settings'))
        self.assertContains(response, '1testoneaccount')

    def test_user_profile(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(
            reverse('profile', kwargs={'name': user.username}))
        self.assertEqual(response.status_code, 200)
