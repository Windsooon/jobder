import json
import django
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client


class PageTestCase(TestCase):

    def test_front_page_200(self):
        # frontpage
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
