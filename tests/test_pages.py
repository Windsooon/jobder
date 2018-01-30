import json
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from tests.base import create_one_account
from common.const import FIND, LOGIN, BROWSE, RANDOM
from post.models import Post


class PageTestCase(TestCase):

    def test_front_page_200_without_login(self):
        response = self.client.get(reverse('front_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, LOGIN)
        self.assertContains(response, BROWSE)
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(reverse('front_page'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, LOGIN)
        self.assertContains(response, FIND)
        self.assertContains(response, BROWSE)

    def test_browse_page_200_with_without_login(self):
        user = create_one_account()
        self.client.force_login(user)
        Post.objects.create(
            user=user,
            title='Senior Software Engineer',
            job_des='You are a self-starter who can work with little',
            onsite=0,
            visa=0,
            salary='$100k',
            company_name='Built For Me Inc.',
            company_des='We are a small company loathe to use the word.',
            location='LA',
            website='https://www.example.com',
            apply='https://job.example.com',
            pay=1,
            pay_time=timezone.now())
        self.client.logout()
        response = self.client.get(reverse('browse'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, RANDOM)

    def test_footer_details(self):
        response = self.client.get(reverse('front_page'))
        self.assertContains(response, 'Created This Awesome Template')

    def test_pages_not_login_redirect(self):
        expected_url = '/accounts/login/?next=/settings/'
        response = self.client.get(reverse('settings'))
        self.assertRedirects(
            response, expected_url, status_code=302, target_status_code=200)

        response = self.client.get(reverse('post_job'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('contributors'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('posted_jobs'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('match'))
        self.assertEqual(response.status_code, 302)

    def test_pages_not_login_browse_job(self):
        response = self.client.get(reverse('browse'))
        self.assertEqual(response.status_code, 200)

    def test_user_login_frontpage_settings(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(reverse('settings'))
        self.assertContains(response, '1testoneaccount')

    def test_user_profile_visiable_without_login(self):
        user = create_one_account()
        response = self.client.get(
            reverse('profile', kwargs={'name': user.username}))
        self.assertEqual(response.status_code, 302)

    def test_user_profile_visiable_with_login(self):
        user = create_one_account()
        response = self.client.get(
            reverse('profile', kwargs={'name': user.username}))
        self.assertEqual(response.status_code, 302)
        self.client.force_login(user)
        response = self.client.get(
            reverse('profile', kwargs={'name': user.username}))
        self.assertEqual(response.status_code, 200)


    def test_user_profile_visiable_by_owner(self):
        user = create_one_account()
        self.client.force_login(user)
        details = {'visiable': 0}
        response = self.client.patch(
            '/api/settings/' + str(user.id) + '/',
            json.dumps(details), content_type='application/json'
        )
        # Visiable by owner
        response = self.client.get(
            reverse('profile', kwargs={'name': user.username}))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        # Non visiable by other users
        response = self.client.get(
            reverse('profile', kwargs={'name': user.username}))
        self.assertTemplateUsed('404.html')

    def test_post_job_pages(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(
            reverse('post_job'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Job Details')

    def test_browse_job_pages(self):
        response = self.client.get(
            reverse('browse'))
        self.assertEqual(response.status_code, 200)
