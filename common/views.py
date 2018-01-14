import json
import base64
import datetime
import random
import requests
from operator import itemgetter
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Case, When
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialToken
from post.models import Post
from jobs.set_logging import setup_logging
from .query import get_repos_query
from .const import FIND, LOGIN, TITLE, POSTED

init_logging = setup_logging()
logger = init_logging.getLogger(__name__)


def index(request):
    '''Front page'''
    return render(request, 'index.html', {'FIND': FIND, 'LOGIN': LOGIN})


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


def browser(request):
    '''Browser job page'''
    ori_posts = Post.objects.filter(pay=1).filter(
        pay_time__gte=timezone.now()
        - datetime.timedelta(days=60)).order_by('id')
    count = ori_posts.count()
    first_id = ori_posts.first().id
    lst = random.sample(range(first_id, first_id + count), count//2)
    posts = Post.objects.filter(id__in=lst)
    return render(request, 'match.html', {'posts': posts, 'title': POSTED})


@login_required
def posted_jobs(request):
    posts = Post.objects.filter(user_id=request.user.id)
    return render(request, 'match.html', {'posts': posts, 'title': POSTED})


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
            ((timezone.now() -
                datetime.timedelta(days=30)) > job.pay_time):
            logger.info('job id %s hasn\'t pay or it\'s expired.' % id)
            if request.user != job.user:
                return render(request, '404.html')
    return render(
        request, 'job.html',
        {
            'repos': [r.repo_name for r in job.repo.all()], 'job': job,
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
        pay_time__gte=timezone.now()
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
    # https://stackoverflow.com/questions/4916851/django-get-a-queryset-from-array-of-ids-in-specific-order
    posts_id = [list(l.keys())[0] for l in lst]
    preserved = Case(
        *[When(pk=pk, then=pos) for pos, pk in enumerate(posts_id)])
    posts = Post.objects.filter(id__in=posts_id).order_by(preserved)
    return render(request, 'match.html', {'posts': posts, 'title': POSTED})
