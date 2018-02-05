from collections import namedtuple
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
from post.models import Post, Repo


def create_repo(n):
    Repos = namedtuple('Repo', 'id, name, language, description')
    r1 = Repos(
        4164482, 'django', 'python',
        'The Web framework for perfectionists with deadlines.')
    r2 = Repos(
        460078, 'angular.js', 'javascript',
        'AngularJS - HTML enhanced for web apps!')
    r3 = Repos(
        2325298, 'linux', 'c',
        'Linux kernel source tree')
    repos = [r1, r2, r3]
    repo = Repo.objects.update_or_create(
        repo_id=repos[n].id,
        defaults={
            'repo_name': repos[n].name,
            'owner_name': 'django',
            'stargazers_count': 31000,
            'description': repos[n].description,
            'language': repos[n].language,
            'html_url': 'https://github.com/django/django'})
    return repo[0]


def create_one_account(username='1testoneaccount', email='1@onexample.com'):
    user = get_user_model().objects.create_user(
            username=username,
            password='1testonepassword',
            email=email)

    app = SocialApp.objects.create(
        provider='GitHub',
        name='GitHub',
        client_id='wienrfdsifnin',
        secret='jiewninrwer',
        key=1)

    account = SocialAccount.objects.create(
        user_id=user.id,
        provider='GitHub',
        uid=184843 + user.id,
        extra_data={"login": "Windsooon", "id": 14333046 + user.id, "avatar_url": "https://avatars2.githubusercontent.com/u/14333046?v=4", "gravatar_id": "", "url": "https://api.github.com/users/Windsooon", "html_url": "https://github.com/Windsooon", "name": "Windson yang", "company": "unicooo", "blog": "https://unicooo.com/Windson/act_create/", "location": "China", "email": "wiwindson@outlook.com", "bio": "Hello, If you wanna know more about me", "public_repos": 54, "public_gists": 2, "created_at": "2015-09-17T15:15:16Z", "updated_at": "2018-01-18T04:14:36Z"})

    SocialToken.objects.create(
        token='96a4b09869718ce8d6e46a3488402353ef63c656',
        account=account,
        app=app)

    repo1 = create_repo(0)
    repo2 = create_repo(1)
    user.settings.repo.add(repo1, repo2)
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

CUSTOMER_RETURN = '''
{
  "account_balance": 0,
  "created": 1517733776,
  "currency": null,
  "default_source": "card_1Brj5PADXywKZUxWOdHzYIXM",
  "delinquent": false,
  "description": "Customer for test username",
  "discount": null,
  "email": "test@user.com",
  "id": "cus_CGFa0zuiwqxHv1",
  "invoice_prefix": "582a1ca81c",
  "livemode": false,
  "metadata": {
    "address_line1": "test address",
    "username": "test username",
    "zip": "51000"
  },
  "object": "customer",
  "shipping": null,
  "sources": {
    "data": [
      {
        "address_city": null,
        "address_country": null,
        "address_line1": "test address",
        "address_line1_check": "pass",
        "address_line2": null,
        "address_state": null,
        "address_zip": "51000",
        "address_zip_check": "pass",
        "brand": "Visa",
        "country": "US",
        "customer": "cus_CGFa0zuiwqxHv1",
        "cvc_check": "pass",
        "dynamic_last4": null,
        "exp_month": 4,
        "exp_year": 2022,
        "fingerprint": "MAQGnAgYtKN8HMLu",
        "funding": "credit",
        "id": "card_1Brj5PADXywKZUxWOdHzYIXM",
        "last4": "4242",
        "metadata": {},
        "name": "test username",
        "object": "card",
        "tokenization_method": null
      }
    ],
    "has_more": false,
    "object": "list",
    "total_count": 1,
    "url": "/v1/customers/cus_CGFa0zuiwqxHv1/sources"
  },
  "subscriptions": {}
}
'''

SUBSCRIPTION_RETURN = '''
{
  "application_fee_percent": null,
  "billing": "charge_automatically",
  "cancel_at_period_end": false,
  "canceled_at": null,
  "created": 1517735040,
  "current_period_end": 1520154240,
  "current_period_start": 1517735040,
  "customer": "cus_CGFvEUfzowI3qE",
  "days_until_due": null,
  "discount": null,
  "ended_at": null,
  "id": "sub_CGFvVM50Z7vYWI",
  "items": {
    "data": [
      {
        "created": 1517735040,
        "id": "si_CGFvBqGq1Y8m25",
        "metadata": {},
        "object": "subscription_item",
        "plan": {
          "amount": 6900,
          "created": 1516281947,
          "currency": "usd",
          "id": "monthly-plan",
          "interval": "month",
          "interval_count": 1,
          "livemode": false,
          "metadata": {},
          "name": "Month Plan",
          "object": "plan",
          "statement_descriptor": null,
          "trial_period_days": null
        },
        "quantity": 1,
        "subscription": "sub_CGFvVM50Z7vYWI"
      }
    ],
    "has_more": false,
    "object": "list",
    "total_count": 1,
    "url": "/v1/subscription_items?subscription=sub_CGFvVM50Z7vYWI"
  },
  "livemode": false,
  "metadata": {},
  "object": "subscription",
  "plan": {
    "amount": 6900,
    "created": 1516281947,
    "currency": "usd",
    "id": "monthly-plan",
    "interval": "month",
    "interval_count": 1,
    "livemode": false,
    "metadata": {},
    "name": "Month Plan",
    "object": "plan",
    "statement_descriptor": null,
    "trial_period_days": null
  },
  "quantity": 1,
  "start": 1517735040,
  "status": "active",
  "tax_percent": null,
  "trial_end": null,
  "trial_start": null
}
'''

USER_REPO = '''
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
              "name": "django"
            }
          }
        ]
      }
    }
  }
}
'''
