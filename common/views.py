import json
import base64
import datetime
import requests
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialToken
from post.models import Post, Repo
from jobs.set_logging import setup_logging
from .query import get_repos_query

init_logging = setup_logging()
logger = init_logging.getLogger(__name__)


def index(request):
    '''Front page'''
    return render(request, 'index.html')


def profile(request, name):
    '''Profile page'''
    user = get_object_or_404(get_user_model(), username=name)
    # other users can see the profile if not visiable
    if not user.settings.visiable:
        if request.user.username == name:
            return render(request, 'profile.html')
        else:
            return render(request, '404.html')
    return render(request, 'profile.html')


def settings(request):
    '''Settings page'''
    if request.user.is_authenticated:
        return render(request, 'settings.html')
    else:
        return render(request, '404.html')


def post_job(request):
    '''Post job page'''
    return render(request, 'post_job.html')


def job(request, id):
    '''job page'''
    onsite = ['Both', 'Remote', 'Onsite']

    try:
        job = Post.objects.get(id=id)
    except Post.DoesNotExist:
        logger.info('job id %s not found' % id)
        return render(request, '404.html')
    else:
        # not pay yet or expired
        if not job.pay or \
            ((datetime.datetime.now() -
                datetime.timedelta(days=30)) > job.pay_time):
            logger.info('job id %s hasn\'t pay or it\'s expired.' % id)
            if request.user != job.user:
                return render(request, '404.html')
    return render(
        request, 'job.html',
        {
            'job': job,
            'onsite': onsite[job.onsite],
            'salary': job.salary})


def match(request):
    '''
    Find the most match jobs
    '''
    try:
        social_token = SocialToken.objects.get(
            account__user__id=request.user.id)
    except SocialToken.DoesNotExist:
        logger.error('Can\'t find token mathc user %s' % request.username)
    # Get user created/contributed repos
    query = get_repos_query(request.user.username, 2)
    headers = {'Authorization': 'bearer ' + social_token.token}
    r = requests.post(
        'https://api.github.com/graphql',
        json.dumps({"query": query}), headers=headers)
    repo = [repo['node']['id'] for repo in r.json()['data']['user']['repositories']['edges']]
    repo_contributedto = [repo['node']['id'] for repo in r.json()['data']['user']['repositoriesContributedTo']['edges']]
    # repo contains a list of repo ids [14400303, 1404040]
    repo.extend(repo_contributedto)

    post_set = Post.objects.filter(pay=1).filter(
        pay_time__gte=datetime.datetime.now()
        -datetime.timedelta(days=60))

    lst = []
    for post in post_set:
        dic = {'id': post.id, 'repos_lst': []}
        for r in post.repo.all():
            dic['repos_lst'].append(r.repo_id)
        lst.append(dic)

    finally_lst = []
    for l in lst:
        dic = {'id': l['id'], 'repos_len': 0}
        dic['repos_len'] = len(set(repo) & set(l['repos_lst']))
        finally_lst.append(dic) 

    logger.debug(finally_lst)
