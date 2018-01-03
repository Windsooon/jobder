import os
import json
import requests
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'jobs.settings'
django.setup()
from popular.models import Popular


def index():
    query_begin = (
        '{ search(query: "stars:>3000", type: REPOSITORY, first: 100, ')
    query_middle = 'after:) {'
    query = '''repositoryCount
        edges {
          cursor
          node {
            ... on Repository {
              id
              name
              nameWithOwner
              description
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

    token = '0e7c6c5a3e6e935292af91c33b1d773fd0375293'
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
            Popular.objects.update_or_create(
                globle_id=d['node']['id'],
                defaults={
                    'name': d['node']['name'],
                    'name_with_owner': d['node']['nameWithOwner'],
                    'description': d['node']['description'],
                    'url': d['node']['url'],
                    'homepage_url': d['node']['homepageUrl'],
                    'primary_language': (
                        d['node']['primaryLanguage']['name']
                        if d['node']['primaryLanguage'] else ""),
                    'star_count': d['node']['stargazers']['totalCount']
                }
            )
        print(last_cursor)
index()
