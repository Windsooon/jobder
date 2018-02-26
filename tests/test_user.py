import json
from unittest import mock
from unittest.mock import patch
from django.test import TestCase
from common.views import _get_user_repos
from tests.base import create_one_account, USER_REPO


class UserTestCase(TestCase):

    @patch('requests.post')
    def test_get_user_repos(self, requests):
        mock_response = mock.Mock()
        mock_response.json.return_value = json.loads(USER_REPO)
        requests.return_value = mock_response
        response = _get_user_repos('Windsooon')
        self.assertEqual(response.json(), json.loads(USER_REPO))
