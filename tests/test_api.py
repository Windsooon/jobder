import json
from django.test import TestCase
from tests.base import create_one_account


class ApiTestCase(TestCase):

    def setUp(self):
        self.user = create_one_account()
        self.user2 = create_one_account('2testaccouont', '2@example.com')
        self.client.force_login(self.user)
        # create job post

    def test_settings_visiable(self):
        details = {
            'blog': 'https://www.testblog.com',
            'linkedin': 'https://www.linkedin.com',
            'location': 2,
            'visiable': False
        }
        self.client.put(
            '/api/settings/' + str(self.user.id) + '/',
            json.dumps(details), content_type="application/json"
        )
        response = self.client.get(
            '/api/settings/' + str(self.user.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.get(
            '/api/settings/' + str(self.user.id) + '/')
        self.assertEqual(response.status_code, 403)
