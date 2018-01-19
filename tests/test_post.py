import json
from django.test import TestCase
from django.urls import reverse
from tests.base import create_one_account, create_one_job


class PageTestCase(TestCase):

    def setUp(self):
        self.user = create_one_account()
        self.user2 = create_one_account('2testaccouont', '2@example.com')
        self.client.force_login(self.user)
        # create job post

    def test_create_job(self):
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
        id = response.json()['id']
        # Posted jobs list on navbar
        response = self.client.get(reverse('front_page'))
        self.assertContains(response, 'Jobs Created')
        # Access job detail
        response = self.client.get(
            reverse('job', kwargs={'id': id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'This job has not been post. ' +
            'Click bottom button to pay.')
        self.assertContains(
            response, 'Senior Software Engineer')
        self.assertContains(
            response, 'Pay $69 per month')

    def test_posted_jobs_show_up_after_created(self):
        response = self.client.get(reverse('front_page'))
        self.assertNotContains(response, 'Posted jobs')

    def test_posted_job_show_up(self):
        create_one_job(self.user.id)
        response = self.client.get(reverse('posted_jobs'))
        self.assertContains(response, 'Senior Software Engineer')

    def test_posted_job_not_show_up(self):
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.get(reverse('posted_jobs'))
        self.assertNotContains(response, 'Senior Software Engineer')
