import os
import base64
import json
import requests
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'jobs.settings'
django.setup()
from post.models import Repo


def index():
    query_begin = (
        '{ search(query: "stars:5000..8122", type: REPOSITORY, first: 100, ')
    query_middle = 'after:) {'
    query = '''repositoryCount
        edges {
          cursor
          node {
            ... on Repository {
              id
              name
              nameWithOwner
              url
              homepageUrl
              primaryLanguage {
                name
              }
              stargazers {
                totalCount
              }
              updatedAt
            }
          }
        }
        pageInfo {
          hasNextPage
        }
      }
    }'''

    token = '358eab55cf28b2ac7c5a66d3bf3fab0411060e86'
    headers = {'Authorization': 'bearer ' + token}
    next_page = True
    last_cursor = 'Y3Vyc29yOjE'
    while next_page:
        query_middle = 'after: "' + last_cursor + '") {'
        lst = [query_begin, query_middle, query]
        finally_query = ''.join(lst)
        r = requests.post(
            'https://api.github.com/graphql',
            json.dumps({"query": finally_query}), headers=headers)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)
            break
        next_page = r.json()['data']['search']['pageInfo']['hasNextPage']
        data = r.json()['data']['search']['edges']
        last_cursor = data[-1]["cursor"]
        # insert data to database
        for d in data:
            Repo.objects.update_or_create(
                repo_id=int(base64.b64decode(d['node']['id'])[14:]),
                defaults={
                    'repo_name': d['node']['name'],
                    'owner_name': d['node']['nameWithOwner'],
                    'url': d['node']['url'],
                    'html_url': d['node']['homepageUrl'],
                    'language': (
                        d['node']['primaryLanguage']['name']
                        if d['node']['primaryLanguage'] else ""),
                    'stargazers_count': d['node']['stargazers']['totalCount']
                }
            )
index()
