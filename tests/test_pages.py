import json
from django.test import TestCase
from django.urls import reverse
from tests.base import create_one_account
from common.const import FIND, LOGIN, BROWSER


class PageTestCase(TestCase):

    def test_front_page_200_without_login(self):
        # frontpage
        response = self.client.get(reverse('front_page'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, FIND)
        self.assertContains(response, LOGIN)
        self.assertContains(response, BROWSER)

    def test_front_page_200_with_login(self):
        # frontpage
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(reverse('front_page'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, LOGIN)
        self.assertContains(response, FIND)
        self.assertContains(response, BROWSER)

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

    def test_pages_not_login_browse_job(self):
        response = self.client.get(reverse('browse'))
        self.assertEqual(response.status_code, 200)

    def test_user_login_frontpage_settings(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(reverse('settings'))
        self.assertContains(response, '1testoneaccount')

    def test_user_profile_visiable_without_login(self):
        user = create_one_account()
        response = self.client.get(
            reverse('profile', kwargs={'name': user.username}))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_visiable_by_owner(self):
        user = create_one_account()
        self.client.force_login(user)
        details = {'visiable': 0}
        response = self.client.patch(
            '/api/settings/' + str(user.id) + '/',
            json.dumps(details), content_type='application/json'
        )
        # Visiable by owner
        response = self.client.get(
            reverse('profile', kwargs={'name': user.username}))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        # Non visiable by other users
        response = self.client.get(
            reverse('profile', kwargs={'name': user.username}))
        self.assertTemplateUsed('404.html')

    def test_post_job_pages(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(
            reverse('post_job'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Job Details')

    def test_browse_job_pages(self):
        response = self.client.get(
            reverse('browse'))
        self.assertEqual(response.status_code, 200)
