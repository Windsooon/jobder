import json
from django.test import TestCase
from django.urls import reverse
from tests.accounts import create_one_account


class PageTestCase(TestCase):

    def setUp(self):
        self.user = create_one_account()
        self.client.force_login(self.user)
        # create job post


    def test_create_job(self):
        job_details = {
	    'title': 'Senior Software Engineer',
            'job_des': 'You are a self-starter who can work with little supervision. You are meticulous about details and sufficiently passionate to get things done, yet know when to pivot to a more experimental move-fast mode. You should be a great teammate who looks to make your colleagues more productive because you know they are doing the same for you.',
	    'company_name': 'Built For Me Inc.',
	    'company_des': 'We are a small company loathe to use the word “startup”. The phrase that most aptly describes us is “boutique consulting firm” as we are currently working on select software consulting projects and have a long term vision to build a stand-alone product in about a year. The future product will focus on enabling business workflows and growing workplace productivity. We are being smart in our approach balancing software consulting with our own product. We balance both to pay ourselves well and support our vision for the future.',
	    'location': 'Seattle, New York, San Francisco',
            'repos': [{'id': 4164482, 'name': 'django', 'owner_name': 'django', 'html_url': 'https://github.com/django/django'}],
	    'salary': '$150k',
            'apply': 'https://angel.co/builtforme/jobs/',
	    'user': self.user.id
        }

        response = self.client.post(
            '/api/post/',
            json.dumps(job_details), content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
