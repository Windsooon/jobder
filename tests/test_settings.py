import json
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from .accounts import create_one_account


class SettingsTestCase(TestCase):

    def test_settings_default_empty(self):
        details = {
            'blog': 'https://www.blog.com',
            'linkedin': 'https://www.linkedin.com',
            'location': 2,
            'visiable': True
        }
        c = Client()
        user = create_one_account()
        c.force_login(user)
        response = c.put(
            '/api/settings/' + str(user.id) + '/',
            json.dumps(details), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('settings'))
        print(response.content)
        self.assertContains(response, 'https://www.blog.com')
