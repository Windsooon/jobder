from django.test import TestCase
from common import views
from tests.base import create_one_account, create_one_job


class FunctionTestCase(TestCase):

    def test_get_valid_post(self):
        self.user = create_one_account()
        self.client.force_login(self.user)
        self.post = create_one_job(self.user.id, pay=True)
        self.post2 = create_one_job(
            self.user.id, title='Backend Engineer',
            pay=True, repo_id=1, type=1)
        self.post3 = create_one_job(
            self.user.id, title='Data Scientist',
            pay=True, repo_id=2, type=2)
        post = views._get_valid_post()
        self.assertEqual(post.count(), 3)
        remote_post = views._get_valid_post(type='remote')
        self.assertEqual(remote_post.count(), 2)

    def test_update_percentage(self):
        lst = [('Python', 25), ('JavaScript', 10), ('CSS', 5)]
        dic = views._update_percentage(lst)
        self.assertEqual(
            dic, {'CSS': 0.125, 'JavaScript': 0.25, 'Python': 0.625})

    def test_pay_post(self):
        self.user = create_one_account()
        self.client.force_login(self.user)
        self.post = create_one_job(self.user.id)
        response = views._pay_post(999)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.post.pay, False)
        response = views._pay_post(self.post.id)
        self.post.refresh_from_db()
        self.assertEqual(self.post.pay, True)
