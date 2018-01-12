import json
from django.test import TestCase
from django.urls import reverse
from tests.base import create_one_account


class SettingsTestCase(TestCase):

    def setUp(self):
        self.user = create_one_account()
        self.client.force_login(self.user)

    def test_settings_default_empty(self):
        response = self.client.get(reverse('settings'))
        self.assertNotContains(response, 'https://www.testblog.com')

    def test_settings_put_change(self):
        details = {
            'blog': 'https://www.testblog.com',
            'linkedin': 'https://www.linkedin.com',
            'location': 2,
            'visiable': True
        }
        response = self.client.put(
            '/api/settings/' + str(self.user.id) + '/',
            json.dumps(details), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('settings'))
        self.assertContains(response, 'https://www.testblog.com')
        self.assertContains(response, 'https://www.linkedin.com')
