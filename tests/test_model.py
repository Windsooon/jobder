from django.test import TestCase
from tests.base import create_repo, create_one_account


class ModelTestCase(TestCase):

    def test_repo_str(self):
        repo = create_repo(0)
        self.assertEqual(str(repo), 'django/django')

    def test_create_settings_model(self):
        user = create_one_account()
        self.assertEqual(user.settings.user_id, user.id)
