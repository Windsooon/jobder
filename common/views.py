import json
import base64
import datetime
import requests
from operator import itemgetter
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialToken
from post.models import Post
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


@login_required
def settings(request):
    '''Settings page'''
    return render(request, 'settings.html')


@login_required
def post_job(request):
    '''Post job page'''
    return render(request, 'post_job.html')


@login_required
def posted_jobs(request):
    '''Posted jobs page'''
    return render(request, 'posted_jobs.html')


def job(request, id):
    '''job page'''
    onsite = ['Onsite And Remote', 'Remote', 'Onsite']

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
            'repos': [r.repo_name for r in job.repo.all()],
            'job': job,
            'onsite': onsite[job.onsite],
            'salary': job.salary})


@login_required
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
    response = requests.post(
        'https://api.github.com/graphql',
        json.dumps({"query": query}), headers=headers)
    repo = [
        r['node']['id'] for r in
        response.json()['data']['user']['repositories']['edges']]
    repo_contributedto = [
        r['node']['id'] for r in
        response.json()['data']['user']['repositoriesContributedTo']['edges']]
    repo.extend(repo_contributedto)
    # repo contains a list of repo ids [14400303, 1404040]
    repo = [int(base64.b64decode(r)[14:]) for r in repo]

    post_set = Post.objects.filter(pay=1).filter(
        pay_time__gte=datetime.datetime.now()
        - datetime.timedelta(days=60))

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
    posts_id = [list(l.keys())[0] for l in lst]
    posts = Post.objects.filter(id__in=posts_id)
    return render(request, 'match.html', {'posts': posts})
