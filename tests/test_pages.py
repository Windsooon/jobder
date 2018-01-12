from django.test import TestCase
from django.urls import reverse
from tests.accounts import create_one_account


class PageTestCase(TestCase):

    def test_front_page_200(self):
        # frontpage
        response = self.client.get(reverse('front_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in with Github')

    def test_pages_not_login_redirect(self):
        expected_url = '/accounts/login/?next=/settings/'
        response = self.client.get(reverse('settings'))
        self.assertRedirects(
            response, expected_url, status_code=302, target_status_code=200)

        response = self.client.get(reverse('post_job'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('posted_jobs'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('match'))
        self.assertEqual(response.status_code, 302)

    def test_user_login_frontpage_settings(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(reverse('front_page'))
        self.assertNotContains(response, 'Log in with Github')
        self.assertContains(response, 'Find a Job')
        response = self.client.get(reverse('settings'))
        self.assertContains(response, '1testoneaccount')

    def test_user_profile_without_login(self):
        user = create_one_account()
        response = self.client.get(
            reverse('profile', kwargs={'name': user.username}))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_login(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(
            reverse('profile', kwargs={'name': user.username}))
        self.assertEqual(response.status_code, 200)

    def test_post_job(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(
            reverse('post_job'))
        self.assertEqual(response.status_code, 200)
