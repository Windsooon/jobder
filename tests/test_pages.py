import json
from unittest.mock import patch
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from tests.base import create_one_account, create_one_job
from common.const import MATCH, LOGIN, JOBLIST, SEARCH
from post.models import Post
from tests.base import GITHUB_REPO_RETURN


class PageTestCase(TestCase):

    def test_front_page_200_with_without_login(self):
        response = self.client.get(reverse('front_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, LOGIN)
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(reverse('front_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, MATCH)

    def test_browse_page_200_with_without_login(self):
        user = create_one_account()
        self.client.force_login(user)
        Post.objects.create(
            user=user,
            title='Senior Software Engineer',
            job_des='You are a self-starter who can work with little',
            type=0,
            visa=0,
            salary='$100k',
            company_name='Built For Me Inc.',
            company_des='We are a small company loathe to use the word.',
            location='LA',
            website='https://www.example.com',
            apply='https://job.example.com',
            pay=1,
            pay_time=timezone.now())
        response = self.client.get(reverse('front_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jobs Posted')
        self.client.logout()
        response = self.client.get(reverse('browse'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Senior Software Engineer')

    def test_explain_page(self):
        response = self.client.get(reverse('explain'))
        self.assertContains(response, 'Why you built Open Source Jobs')
        self.assertContains(response, 'Q & A')
        self.assertEqual(response.status_code, 200)

    def test_browse_no_post(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(reverse('browse'))
        self.assertContains(response, JOBLIST)
        self.assertNotContains(response, 'Senior Software Engineer')
        self.assertContains(response, 'Show Remote Jobs')
        self.assertEqual(response.status_code, 200)

    def test_other_pages_not_login_redirect(self):
        # Before user login
        response = self.client.get(reverse('post_job'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('pay'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('repo_search'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('match'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('match'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('contributors'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('posted_jobs'))
        self.assertEqual(response.status_code, 302)
        # After user login
        user = create_one_account()
        self.client.force_login(user)
        self.post = create_one_job(user.id)
        response = self.client.get(reverse('contributors'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, SEARCH)
        response = self.client.get(reverse('posted_jobs'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('post_job'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Job Details')

    @patch('common.views._get_user_repos')
    def test_find_your_match(self, repos):

        class Repo:
            @classmethod
            def json(cls):
                return json.loads(GITHUB_REPO_RETURN)

        self.user = create_one_account()
        self.client.force_login(self.user)
        self.post = create_one_job(self.user.id, pay=True)
        self.post2 = create_one_job(
            self.user.id, title='Backend Engineer', pay=True, repo_id=1)
        self.post3 = create_one_job(
            self.user.id, title='Data Scientist', pay=True, repo_id=2)
        repos.return_value = Repo
        response = self.client.get(reverse('match'))
        self.assertContains(response, '<a class="job-title"')
        self.assertContains(response, 'Senior Software Engineer')
        self.assertContains(
            response, '<i class="fa fa-building building"')

    @patch('common.views._get_user_repos')
    def test_find_your_match_with_remote(self, repos):

        class Repo:
            @classmethod
            def json(cls):
                return json.loads(GITHUB_REPO_RETURN)

        self.user = create_one_account()
        self.client.force_login(self.user)
        self.post = create_one_job(self.user.id, pay=True, type=2, repo_id=0)
        self.post2 = create_one_job(
            self.user.id, title='Backend Engineer', pay=True, repo_id=1)
        self.post3 = create_one_job(
            self.user.id, title='Data Scientist', pay=True, repo_id=2)
        self.post4 = create_one_job(
            self.user.id, title='Frontend Engineer', pay=True, repo_id=1)
        repos.return_value = Repo
        response = self.client.get('/match/?type=remote')
        self.assertContains(response, '<a class="job-title"')
        self.assertNotContains(response, 'Senior Software Engineer')
        self.assertContains(response, 'Backend Engineer')
        self.assertContains(
            response, '<i class="fa fa-building building"')

    def test_repo_search_miss_id(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(reverse('repo_search'))
        self.assertEqual(response.status_code, 400)

    def test_repo_search_no_valid_post_user(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get("%s?repo_id=1" % (reverse('repo_search')))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"length": 0, "data": []})

    @patch('common.views._get_user_repos')
    def test_repo_search_valid_post_user(self, repos):
        class Repo:
            @classmethod
            def json(cls):
                return json.loads(GITHUB_REPO_RETURN)
        repos.return_value = Repo
        user = create_one_account()
        self.client.force_login(user)
        create_one_job(user.id, pay=True)
        response = self.client.get(reverse('match'))
        response = self.client.get(
            "%s?repo_id=4164482" % (reverse('repo_search')))
        user_response = {
            'length': 1,
            'data': [{
                'username': '1testoneaccount',
                'avatar_url':
                    'https://avatars2.githubusercontent.com/u/14333046?v=4'}
            ]
        }
        self.assertEqual(response.json(), user_response)

    def test_no_card(self):
        user = create_one_account()
        self.client.force_login(user)
        response = self.client.get(
            reverse('card', kwargs={'name': user.username}))
        self.assertContains(
            response, 'You don\'t have any card yet.')
