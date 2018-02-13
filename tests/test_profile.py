import json
from django.test import TestCase
from django.urls import reverse
from tests.base import create_one_account


class ProfileTestCase(TestCase):

    def setUp(self):
        self.user = create_one_account()
        self.user2 = create_one_account('2testaccouont', '2@example.com')

    def test_user_profile_visiable_or_not_with_login(self):
        response = self.client.get(
            reverse('profile', kwargs={'name': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('profile', kwargs={'name': self.user.username}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('profile', kwargs={'name': self.user2.username}))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_only_visiable_by_owner(self):
        self.client.force_login(self.user)
        details = {'visiable': 0}
        response = self.client.patch(
            '/api/settings/' + str(self.user.id) + '/',
            json.dumps(details), content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        # Visiable by owner
        response = self.client.get(
            reverse('profile', kwargs={'name': self.user.username}))
        self.assertEqual(response.status_code, 200)
        # Non visiable by other users
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.get(
            reverse('profile', kwargs={'name': self.user.username}))
        self.assertEqual(response.status_code, 404)

    def test_user_profile_button_text(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('profile', kwargs={'name': self.user.username}))
        self.assertInHTML(
            '<a href="/match/" class="btn btn-default btn-lg" ' +
            'title="">Find Your Match</a>', response.content.decode('utf-8'))
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.get(
            reverse('profile', kwargs={'name': self.user.username}))
