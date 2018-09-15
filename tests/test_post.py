import json
import datetime
from unittest.mock import patch
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from common.models import Customer
from common.views import charge_su
from tests.base import create_one_account, create_one_job,\
    CUSTOMER_RETURN, SUBSCRIPTION_RETURN


class PostTestCase(TestCase):

    def setUp(self):
        self.user = create_one_account()
        self.user2 = create_one_account('2testaccouont', '2@example.com')
        self.client.force_login(self.user)

    def test_expired_job(self):
        self.post = create_one_job(self.user.id)
        self.post.pay_time = timezone.now()-datetime.timedelta(days=40)
        self.post.save()
        self.post2 = create_one_job(
            self.user.id, title='Backend Engineer', pay=True)
        self.post2.pay_time = timezone.now()-datetime.timedelta(days=20)
        self.post2.save()

        def is_valid_post(post):
            return (
                post.pay and
                post.pay_time > timezone.now()-datetime.timedelta(days=30))
        self.assertFalse(is_valid_post(self.post))
        self.assertTrue(is_valid_post(self.post2))

    def test_create_job_without_pay(self):
        self.post = create_one_job(self.user.id)
        # Posted jobs list on navbar
        response = self.client.get(reverse('front_page'))
        self.assertContains(response, 'Jobs Posted')
        # Access job detail
        response = self.client.get(
            reverse('job', kwargs={'id': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'To pay with your credit card')
        self.assertContains(
            response, 'Senior Software Engineer')
        self.assertContains(
            response, 'Pay $69.3/first month')
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
            response, 'To pay with your credit card')
        self.assertContains(
            response, 'Senior Software Engineer')
        self.assertContains(
            response, 'django')
        self.assertContains(
            response, 'No Visa Support')
        self.assertContains(
            response, 'Onsite And Remote')
        self.assertNotContains(
            response, 'Pay $69.3/first month')
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
        self.assertContains(response, 'Jobs Posted')

    def test_can_not_find_job(self):
        response = self.client.get(reverse('job', kwargs={'id': 10}))
        self.assertEqual(response.status_code, 404)

    def test_browse_show_up_one_third_job(self):
        self.post = create_one_job(self.user.id, pay=True)
        self.post2 = create_one_job(
            self.user.id, title='Backend Engineer', pay=True)
        self.post3 = create_one_job(
            self.user.id, title='Data Scientist', pay=True)
        response = self.client.get(reverse('browse'))
        self.assertContains(response, '<a class="job-title"')
        self.assertContains(response, 'Backend Engineer')
        self.assertContains(
            response, '<i class="fa fa-building building" aria-hidden="true">')

    @staticmethod
    def get_data(post_id):
        return {
            'token': 'tok_1Bri70ADXywKZUxvWPimDJxnJ',
            'card': {
                'id': 'card_1Bri6zADXywKZUxWrbOZa2ZC',
                'address_line1': 'test address',
                'address_zip': '510000',
                'exp_month': 1,
                'exp_year': 2022,
                'last4': "4242",
                'name': 'test username',
            },
            'email': 'test@user.com',
            'post_id': post_id,
        }

    @patch('stripe.Customer.create')
    @patch('stripe.Subscription.create')
    def test_pay(self, subscription, customer):
        # mock return value
        customer.return_value = json.loads(CUSTOMER_RETURN)
        subscription.return_value = json.loads(SUBSCRIPTION_RETURN)
        self.post = create_one_job(self.user.id)
        self.assertEqual(0, Customer.objects.count())
        data = self.get_data(self.post.id)
        response = self.client.post(
            '/pay/',
            json.dumps(data), content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        # Wait for charge.successed callback
        cus = Customer.objects.get(stripe_email='test@user.com')
        self.assertEqual(cus.cus_id, 'cus_CGFa0zuiwqxHv1')
        self.assertEqual(cus.stripe_exp_year, 2022)
        self.assertEqual(1, Customer.objects.count())

        class Data:
            def __init__(self):
                self.body = (
                    b'{"data":'
                    b'{"object": {"customer": "cus_CGFa0zuiwqxHv1"}}}')
        request = Data()
        self.assertEqual(charge_su(request).status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.pay, True)
