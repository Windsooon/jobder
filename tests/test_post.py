from django.test import TestCase
from django.urls import reverse
from tests.base import create_one_account, create_one_job


class PostTestCase(TestCase):

    def setUp(self):
        self.user = create_one_account()
        self.user2 = create_one_account('2testaccouont', '2@example.com')
        self.client.force_login(self.user)
        # create job post

    def test_create_job_without_pay(self):
        self.post = create_one_job(self.user.id)
        # Posted jobs list on navbar
        response = self.client.get(reverse('front_page'))
        self.assertContains(response, 'Jobs Created')
        # Access job detail
        response = self.client.get(
            reverse('job', kwargs={'id': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'This job has not been post. ' +
            'Click bottom button to pay.')
        self.assertContains(
            response, 'Senior Software Engineer')
        self.assertContains(
            response, 'Pay $69 per month')
        self.client.logout()
        response = self.client.get(
            reverse('job', kwargs={'id': self.post.id}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed('404.html')

    def test_create_job_with_pay_show_up(self):
        self.post = create_one_job(self.user.id, pay=True)
        response = self.client.get(
            reverse('job', kwargs={'id': self.post.id}))
        self.assertNotContains(
            response, 'This job has not been post. ' +
            'Click bottom button to pay.')
        self.assertContains(
            response, 'Senior Software Engineer')
        self.assertContains(
            response, 'django')
        self.assertContains(
            response, 'No Visa Support')
        self.assertContains(
            response, 'Onsite And Remote')
        self.assertNotContains(
            response, 'Pay $69 per month')
        self.client.logout()
        response = self.client.get(
            reverse('job', kwargs={'id': self.post.id}))
        self.assertContains(
            response, 'Senior Software Engineer')

    def test_posted_jobs_show_up_after_created(self):
        response = self.client.get(reverse('front_page'))
        self.assertNotContains(response, 'Jobs Created')
        self.post = create_one_job(self.user.id, pay=True)
        response = self.client.get(reverse('front_page'))
        self.assertContains(response, 'Jobs Created')

    def test_browse_show_up_one_third_job(self):
        self.post = create_one_job(self.user.id, pay=True)
        self.post2 = create_one_job(
            self.user.id, title='Backend Engineer', pay=True)
        self.post3 = create_one_job(
            self.user.id, title='Data Scientist', pay=True)
        response = self.client.get(reverse('browse'))
        self.assertContains(response, '<a class="job-title" target="_blank"')
        self.assertContains(
            response, '<i class="fa fa-building building" aria-hidden="true">')

    def test_find_your_match(self):
        self.post = create_one_job(self.user.id, pay=True)
        self.post2 = create_one_job(
            self.user.id, title='Backend Engineer', pay=True)
        self.post3 = create_one_job(
            self.user.id, title='Data Scientist', pay=True)
        # response = self.client.get(reverse('match'))
        # self.assertContains(response, '<a class="job-title" target="_blank"')
        # self.assertContains(
        #     response, '<i class="fa fa-building building"')
