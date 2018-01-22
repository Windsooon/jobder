from django.contrib.auth import get_user_model
from post.models import Post, Repo


def create_one_account(username='1testoneaccount', email='1@onexample.com'):
    return get_user_model().objects.create_user(
            username=username,
            password='1testonepassword',
            email=email)


def create_multi_accounts(number):
    return [get_user_model().objects.create_user(
            username=str(num) + 'testaccount',
            password=str(num) + 'testpassword',
            email=str(num) + '@example.com') for num in range(1, number+1)]


def create_one_job(
        user_id, title='Senior Software Engineer',
        job_des='You are a self-starter who can work with everything.'):
    repo = Repo.objects.create(
            repo_id=459599,
            repo_name='django',
            owner_name='django',
            stargazers_count=10000,
            language='python',
            html_url='https://github.com/django/django')

    post = Post.objects.create(
            title='Senior Software Engineer',
            job_des='You are a self-starter who can work with everything.',
            company_name='Built For Me Inc.',
            company_des='We are a small company use the word "startup".',
            location='Seattle, New York, San Francisco',
            salary='$150k',
            apply='https://angel.co/builtforme/jobs/',
            user_id=user_id)
    post.repo.add(repo)
    return post
