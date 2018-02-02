from collections import namedtuple
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialToken, SocialAccount
from post.models import Post, Repo


def create_one_account(username='1testoneaccount', email='1@onexample.com'):
    user = get_user_model().objects.create_user(
            username=username,
            password='1testonepassword',
            email=email)
    SocialToken.objects.create(
        token='96a4b09869718ce8d6e46a3488402353ef63c656',
        account_id=user.id,
        app_id=1)
    SocialAccount.objects.create(
        user_id=user.id,
        provider='github',
        uid=184843 + user.id,
        extra_data='{"login": "Windsooon", "id": 14333046, "avatar_url": "https://avatars2.githubusercontent.com/u/14333046?v=4", "gravatar_id": "", "url": "https://api.github.com/users/Windsooon", "html_url": "https://github.com/Windsooon", "name": "Windson yang", "company": "unicooo", "blog": "https://unicooo.com/Windson/act_create/", "location": "China", "email": "wiwindson@outlook.com", "bio": "Hello, If you wanna know more about me", "public_repos": 54, "public_gists": 2, "created_at": "2015-09-17T15:15:16Z", "updated_at": "2018-01-18T04:14:36Z"}')
    return user


def create_multi_accounts(number):
    return [get_user_model().objects.create_user(
            username=str(num) + 'testaccount',
            password=str(num) + 'testpassword',
            email=str(num) + '@example.com') for num in range(1, number+1)]


def create_one_job(
        user_id, pay=None, repo_id=0,
        title='Senior Software Engineer',
        job_des='You are a self-starter who can work with everything.'):

    def create_repo(n):
        Repos = namedtuple('Repo', 'id, name, language')
        r1 = Repos(4164482, 'django', 'python')
        r2 = Repos(460078, 'angular.js', 'javascript')
        r3 = Repos(2325298, 'linux', 'c')
        repos = [r1, r2, r3]

        return Repo.objects.create(
            repo_id=repos[n].id,
            repo_name=repos[n].name,
            owner_name='django',
            stargazers_count=31000,
            language=repos[n].language,
            html_url='https://github.com/django/django')

    post = Post.objects.create(
            title='Senior Software Engineer',
            job_des='You are a self-starter who can work with everything.',
            company_name='Built For Me Inc.',
            company_des='We are a small company use the word "startup".',
            location='Seattle, New York, San Francisco',
            salary='$150k',
            apply='https://angel.co/builtforme/jobs/',
            pay=pay if pay else False,
            user_id=user_id)
    repo = create_repo(repo_id)
    post.repo.add(repo)
    return post


GITHUB_REPO_RETURN = '''
{
  "data": {
    "user": {
      "name": "Windson yang",
      "avatarUrl": "https://avatars2.githubusercontent.com/u/14333046?v=4",
      "location": "China",
      "websiteUrl": "https://unicooo.com/Windson/act_create/",
      "email": "wiwindson@outlook.com",
      "bio": "Hello, If you wanna know more about me, please have a look at https://www.unicooo.com/Windson/act_create/ . I also writing blogs at https://windsooon.github.io/",
      "repositories": {
        "edges": [
          {
            "node": {
              "id": "MDEwOlJlcG9zaXRvcnk0MzA1MzM4NQ==",
              "name": "How-to-pronounce",
              "nameWithOwner": "Windsooon/How-to-pronounce",
              "url": "https://github.com/Windsooon/How-to-pronounce",
              "stargazers": {
                "totalCount": 63
              },
              "primaryLanguage": null
            }
          }
        ]
      },
      "repositoriesContributedTo": {
        "edges": [
          {
            "node": {
              "id": "MDEwOlJlcG9zaXRvcnk0MTY0NDgy",
              "name": "django",
              "nameWithOwner": "django/django",
              "url": "https://github.com/django/django",
              "stargazers": {
                "totalCount": 31490
              },
              "primaryLanguage": {
                "name": "Python"
              }
            }
          }
        ]
      }
    }
  }
}
'''
