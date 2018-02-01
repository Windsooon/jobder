import json
import base64
import datetime
import random
import requests
from operator import itemgetter
from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Case, When
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from allauth.account.signals import user_logged_in
from post.models import Post, Repo
from jobs.set_logging import setup_logging
from .query import get_repos_query
from .const import FIND, LOGIN, POSTED, TITLE, RANDOM, STRIPE_API_KEY

init_logging = setup_logging()
logger = init_logging.getLogger(__name__)


def _get_user_repos(user):
    '''
    Get user all repos through Github graphql api
    '''
    social_token = (
        user.socialaccount_set.first().socialtoken_set.first())
    query = get_repos_query(user.username, 100)
    headers = {'Authorization': 'bearer ' + social_token.token}
    return requests.post(
        'https://api.github.com/graphql',
        json.dumps({"query": query}), headers=headers)


def _get_valid_post():
    '''
    Get paid post and valid post
    '''
    return Post.objects.filter(pay=1).filter(
        pay_time__gte=timezone.now()
        - datetime.timedelta(days=30))


def index(request):
    '''Front page'''
    return render(request, 'index.html', {'FIND': FIND, 'LOGIN': LOGIN})


@login_required
def profile(request, name):
    '''Profile page'''
    user = get_object_or_404(get_user_model(), username=name)
    # other users can see the profile if not visiable
    if not user.settings.visiable:
        if request.user.username == name:
            return render(request, 'profile.html', {'user': user})
        else:
            return render(request, '404.html', status=404)
    return render(request, 'profile.html', {'user': user})


@login_required
@csrf_exempt
def token(request):
    import stripe
    stripe.api_key = STRIPE_API_KEY
    data = json.loads(request.body)
    customer = stripe.Customer.create(
        description='Customer for ' + data['name']['name'],
        email=data['email'],
        metadata={
            'username': data['name']['name'],
            'address_line1': data['name']['address_line1']
        },
        source=data['token'],
    )
    request.user.settings.stripe_customer_id = customer['id']
    request.user.settings.stripe_email = customer['email']
    request.user.settings.stripe_name = customer['metadata']['username']
    request.user.settings.stripe_last4 = customer['sources']['data']['last4']
    request.user.settings.stripe_exp_year = customer['sources']['data']['exp_year']
    request.user.settings.stripe_exp_month = customer['sources']['data']['exp_month']
    request.user.settings.stripe_zip = customer['sources']['data']['address_zip']
    request.user.settings.save()

    subscription = stripe.Subscription.create(
        customer=customer['id'],
        items=[
          {
            "plan": "monthly-plan",
          },
        ],
    )
    return HttpResponse(200)


@login_required
def settings(request):
    '''Settings page'''
    return render(request, 'settings.html')


@login_required
def post_job(request):
    '''Post job page'''
    return render(request, 'post_job.html')


@login_required
def contributors(request):
    '''Find contributors'''
    return render(request, 'contributors.html')


@login_required
def repo_search(request):
    '''Search contributors'''
    repo_id = request.GET.get('repo_id', '')
    if repo_id:
        res_lst = []
        # Select user create or contributed to this repo
        user_lst = get_user_model().objects.filter(
            settings__visiable=1).filter(settings__repo__repo_id=repo_id).all()
        length = user_lst.count()
        posts = _get_valid_post()
        if any(post.user_id == request.user.id for post in posts):
            for user in user_lst:
                u = defaultdict(dict)
                extra_data = user.socialaccount_set.first().extra_data
                u['username'] = extra_data['login']
                u['avatar_url'] = extra_data['avatar_url']
                res_lst.append(u)
            return JsonResponse({'length': length, 'data': res_lst})
        else:
            return JsonResponse({'length': -1, 'data': []})
    else:
        return HttpResponse(status_code=400)


@login_required
@csrf_exempt
def pay(request):
    event_json = json.loads(request.body)
    logger.debug(event_json)
    return HttpResponse(status=200)


def browse(request):
    '''Browse job page'''
    ori_posts = _get_valid_post().order_by('id')
    count = ori_posts.count()
    if count:
        first_id = ori_posts.first().id
        lst = random.sample(range(first_id, first_id + count), count*1//3)
        posts = Post.objects.filter(id__in=lst)
        return render(request, 'match.html', {'posts': posts, 'title': RANDOM})
    else:
        return render(request, '404.html', status=404)


@login_required
def posted_jobs(request):
    posts = Post.objects.filter(user_id=request.user.id)
    return render(request, 'match.html', {'posts': posts, 'title': POSTED})


def job(request, id):
    '''job page'''
    onsite = ['Onsite And Remote', 'Remote', 'Onsite']
    visa = ['No Visa Support', 'Visa Support']

    try:
        job = Post.objects.get(id=id)
    except Post.DoesNotExist:
        logger.info('job id %s not found' % id)
        return render(request, '404.html', status=404)
    else:
        # not pay yet or expired
        if not job.pay or \
            ((timezone.now() -
                datetime.timedelta(days=30)) > job.pay_time):
            logger.info('job id %s hasn\'t pay or it\'s expired.' % id)
            if request.user != job.user:
                return render(request, '404.html', status=404)
    return render(
        request, 'job.html',
        {
            'repos': [r.repo_name for r in job.repo.all()], 'job': job,
            'onsite': onsite[job.onsite],
            'visa': visa[job.visa],
            'salary': job.salary})


@login_required
def match(request):
    '''
    Find the most match jobs
    '''
    # Get user created/contributed repos
    response = _get_user_repos(request.user)
    repo = [
        r['node']['id'] for r in
        response.json()['data']['user']['repositories']['edges']]
    repo_contributedto = [
        r['node']['id'] for r in
        response.json()['data']['user']['repositoriesContributedTo']['edges']]
    repo.extend(repo_contributedto)
    # repo contains a list of repo ids [14400303, 1404040]
    repo = [int(base64.b64decode(r)[14:]) for r in repo]

    post_set = _get_valid_post()
    count = post_set.count()
    # lst contain every valid post
    # and its repo id [{'id': 9: 'repos_lst': [621, 1058, 325198]},...]
    lst = []
    for post in post_set:
        dic = {post.id: []}
        for r in post.repo.all():
            dic[post.id].append(r.repo_id)
        lst.append(dic)
    # Repos_len means how many repos match
    for l in lst:
        l['repos_len'] = len(set(repo) & set(list(l.values())[0]))
    lst = sorted(
        lst, key=itemgetter('repos_len'), reverse=True)
    # Post id sorted [16, 9, 10]
    # https://stackoverflow.com/questions/4916851/django-get-a-queryset-from-array-of-ids-in-specific-order
    posts_id = [list(l.keys())[0] for l in lst]
    preserved = Case(
        *[When(pk=pk, then=pos) for pos, pk in enumerate(posts_id)])
    posts = Post.objects.filter(
        id__in=posts_id).order_by(preserved)[:(count*1//3)]
    return render(request, 'match.html', {'posts': posts, 'title': TITLE})


@receiver(user_logged_in)
def after_user_logged_in(sender, **kwargs):
    user = kwargs['user']
    response = _get_user_repos(user)
    repos = response.json()['data']['user']['repositories']['edges']
    repos_contributed = (
        response.json()['data']['user']['repositoriesContributedTo']['edges'])
    repos.extend(repos_contributed)
    repo_lst = []
    for repo in repos:
        if repo['node']['stargazers']['totalCount'] > 200:
            repo_name = repo['node']['name']
            owner_name = repo['node']['nameWithOwner'].split('/')[0]
            if repo['node']['primaryLanguage']:
                language = repo['node']['primaryLanguage']['name']
            else:
                language = ""
            obj, created = Repo.objects.update_or_create(
                repo_id=int(base64.b64decode(repo['node']['id'])[14:]),
                defaults={
                    'repo_name': repo_name,
                    'owner_name': owner_name,
                    'stargazers_count':
                        repo['node']['stargazers']['totalCount'],
                    'language': language,
                    'html_url': repo['node']['url'],
                },
            )
            repo_lst.append(obj.id)
    user.settings.repo.add(*repo_lst)
    logger.info('%s log in' % user.username)
