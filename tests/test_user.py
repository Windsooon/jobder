import json
import django
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from .accounts import create_random_account


class UserTestCase(TestCase):

    def test_user(self):
        user = create_random_account(1)
        # frontpage

