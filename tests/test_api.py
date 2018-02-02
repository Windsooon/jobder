import json
from django.urls import reverse
from django.test import TestCase
from post.models import Post
from common.query import get_repos_query
from tests.base import create_one_account


class ApiTestCase(TestCase):

    def setUp(self):
        self.user = create_one_account()
        self.user2 = create_one_account('2testaccouont', '2@example.com')
        self.client.force_login(self.user)

    def test_create_job(self):
        response = self.client.get(reverse('front_page'))
        self.assertNotContains(response, 'Jobs Created')
        job_details = {
            'title': 'Senior Software Engineer',
            'job_des': 'You are a self-starter who can work with little',
            'company_name': 'Built For Me Inc.',
            'company_des': 'We are a small company loathe to use the word.',
            'location': 'Seattle, New York, San Francisco',
            'repos': [{
                'id': 4164482, 'name': 'django', 'owner_name': 'django',
                'html_url': 'https://github.com/django/django',
                'stargazers_count': 30000, 'language': 'python'}],
            'salary': '$150k',
            'apply': 'https://angel.co/builtforme/jobs/',
            'user': self.user.id
        }

        response = self.client.post(
            '/api/post/',
            json.dumps(job_details), content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.all().count(), 1)

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

    def test_query(self):
        self.assertIn('Windson', get_repos_query('Windson', 100))
