import json
import base64
import datetime
import random
import math
import requests
from operator import itemgetter
from collections import defaultdict, Counter
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, When, Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from post.models import Post, Repo
from common.models import FakeUser, Customer
from jobs.set_logging import setup_logging
from .stripe_method import create_customer_and_subscribe, \
    update_card
from .query import get_repos_query
from .const import MATCH, LOGIN, PROFILE, \
    POSTED, TITLE, JOBLIST, STRIPE_PUB_KEY, TOKEN_LIST

init_logging = setup_logging()
logger = init_logging.getLogger(__name__)
POST_DAY = 30


def _get_user_repos(name):
    '''
    Get user all repos through Github graphql api, (blocking)
    pare
    '''
    token = random.choice(TOKEN_LIST)
    query = get_repos_query(name, 20)
    headers = {'Authorization': 'bearer ' + token}
    return requests.post(
        'https://api.github.com/graphql',
        json.dumps({"query": query}), headers=headers)


def _get_valid_post(type='both'):
    '''
    Get paid posts and valid posts
    '''
    if type == 'remote':
        return Post.objects.filter(pay=1).exclude(type=2).filter(
            pay_time__gte=timezone.now()
            - datetime.timedelta(days=POST_DAY))
    else:
        return Post.objects.filter(pay=1).filter(
            pay_time__gte=timezone.now()
            - datetime.timedelta(days=POST_DAY))


def _update_percentage(lst):
    '''
    : para lst: [('Python', 25), ('JavaScript', 10), ('CSS', 5)]
    '''
    sum_lst_val = sum(l[1] for l in lst)
    # {'Python': 25/40, 'JavaScript': 10/40}
    return {k: v/sum_lst_val for k, v in lst}


def _calculate_points(val, most_dict):
    points = 0
    for v in val:
        if v in most_dict:
            points += most_dict[v]
    return points


def _pay_post(id):
    '''
    Update post status and pay_time
    '''
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        logger.error('Post %s does not exist.' % id)
        return HttpResponse(
            'Post %s does not exist.' % id, status=400)
    else:
        post.pay = True
        post.pay_time = timezone.now()
        post.save()
        return HttpResponse(
            'Post {0} pay successed'.format(id, status=200))


@login_required
@csrf_exempt
def pay(request):
    '''
    First time when user pay for a job
    '''
    data = json.loads(request.body)
    user = request.user
    # update user info
    return create_customer_and_subscribe(user, data)


@login_required
def post_job(request):
    '''Post job page'''
    return render(request, 'post_job.html')


@login_required
def contributors(request):
    '''Find contributors'''
    repos = Repo.objects.annotate(
        q_count=Count('fakeuser')).order_by('-q_count')[:3]
    return render(request, 'contributors.html', {'repos': repos})


@login_required
def repo_search(request):
    '''Search contributors'''
    repo_id = request.GET.get('repo_id', '')
    if repo_id:
        res_lst = []
        # Select user create or contributed to this repo
        fake_user_lst = FakeUser.objects.filter(repo__repo_id=repo_id).all()
        length = fake_user_lst.count()
        posts = _get_valid_post()
        if any(post.user_id == request.user.id for post in posts):
            for user in fake_user_lst:
                u = defaultdict(dict)
                u['username'] = user.username
                u['avatar_url'] = user.avatar_url
                res_lst.append(u)
            return JsonResponse({'length': length, 'data': res_lst})
        else:
            return JsonResponse({'length': length, 'data': []}, status=403)
    else:
        return HttpResponse(status=400)


def browse(request):
    '''Browse job page'''
    type = request.GET.get('type', 'both')
    ori_posts = _get_valid_post(type).order_by('-pay_time')
    return render(
        request, 'match.html',
        {'view': 'browse', 'posts': ori_posts,
            'title': JOBLIST, 'type': type})


@login_required
def posted_jobs(request):
    posts = Post.objects.filter(user_id=request.user.id)
    return render(
        request, 'match.html',
        {'view': 'posted', 'posts': posts, 'title': POSTED})


def index(request):
    '''Front page'''
    return render(
        request, 'index.html',
        {'FIND': MATCH, 'LOGIN': LOGIN, 'PROFILE': PROFILE})


def explain(request):
    '''explain page'''
    return render(request, 'explain.html')


def job(request, id):
    '''job page'''
    type = ['Onsite And Remote', 'Remote', 'Onsite']
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
                datetime.timedelta(days=POST_DAY)) > job.pay_time):
            logger.info('job id %s hasn\'t pay or it\'s expired.' % id)
            if request.user != job.user:
                return render(request, '404.html', status=404)
    return render(
        request, 'job.html',
        {
            'repos': [r.repo_name for r in job.repo.all()], 'job': job,
            'type': type[job.type],
            'visa': visa[job.visa],
            'salary': job.salary})


@login_required
def card(request, name):
    '''Get current card details'''
    settings = request.user.settings
    cards = Customer.objects.filter(settings_id=settings.user_id)
    count = len(cards)
    return render(
        request, 'card.html',
        {'cards': cards,
         'count': count,
         'STRIPE_PUB_KEY': STRIPE_PUB_KEY})


@login_required
@csrf_exempt
def card_callback(request, post_id):
    '''
    Update user's card
    '''
    token = request.POST.get('stripeToken', '')
    email = request.POST.get('stripeEmail', '')
    try:
        cus = Customer.objects.get(post_id=post_id)
    except Customer.ObjectDoesNotExist:
        pass
    if token and email and id:
        response = update_card(cus.cus_id, token, email)
        data = response['sources']['data'][0]
        cus.stripe_email = data['name']
        cus.stripe_exp_year = data['exp_year']
        cus.stripe_exp_month = data['exp_month']
        cus.stripe_last4 = data['last4']
        cus.save()
    return redirect('card', name=request.user.username)


@csrf_exempt
def charge_su(request):
    '''
    charge successed callback event
    '''
    response = json.loads(request.body.decode("utf-8"))
    customer_id = response['data']['object']['customer']
    try:
        cus = Customer.objects.get(cus_id=customer_id)
    except ObjectDoesNotExist:
        return HttpResponse(
            'customer %s doesn\'t exist' % customer_id, status=400)
    else:
        return _pay_post(cus.post_id)


@login_required
def match(request):
    '''
    Find the most match jobs
    '''
    # Get user created/contributed repos

    name = request.user.username

    def _sigmoid(x):
        return 1/(1+math.exp(-x))

    def _sigmoid_to_percentage(x):
        return str(round(_sigmoid(x) * 100)) + '%'

    response = _get_user_repos(name)

    fake_user_obj, created = FakeUser.objects.get_or_create(
            username=name,
            avatar_url=response.json()['data']['user']['avatarUrl']
            )

    repo = response.json()['data']['user']['repositories']['edges']
    repo_contributedto = (
        response.json()['data']['user']['repositoriesContributedTo']['edges'])

    repo.extend(repo_contributedto)

    # save repos
    repo_lst = []
    for r in repo:
        if r['node']['stargazers']['totalCount'] > 200:
            repo_name = r['node']['name']
            owner_name = r['node']['nameWithOwner'].split('/')[0]
            if (r['node']['primaryLanguage']
                    and r['node']['primaryLanguage'] != 'HTML'):
                language = r['node']['primaryLanguage']['name']
            else:
                language = ""
            obj, created = Repo.objects.update_or_create(
                repo_id=int(base64.b64decode(r['node']['id'])[14:]),
                defaults={
                    'repo_name': repo_name,
                    'owner_name': owner_name,
                    'stargazers_count':
                        r['node']['stargazers']['totalCount'],
                    'description': r['node']['description'],
                    'language': language,
                    'html_url': r['node']['url'],
                },
            )
            repo_lst.append(obj.id)
    fake_user_obj.repo.add(*repo_lst)

    repo_languages = [
        r['node']['primaryLanguage']['name'] for r in
        response.json()['data']['user']['repositories']['edges']
        if (r['node']['primaryLanguage'] and
            r['node']['primaryLanguage']['name'] != 'HTML')]
    repo_contributedto_languages = [
        r['node']['primaryLanguage']['name'] for r in
        response.json()['data']['user']['repositoriesContributedTo']['edges']
        if (r['node']['primaryLanguage'] and
            r['node']['primaryLanguage']['name'] != 'HTML')]
    repo_languages.extend(repo_contributedto_languages)
    most_languages_all = [r for r in Counter(repo_languages).most_common(3)]
    most_dict = _update_percentage(most_languages_all)
    # repo is a list contains repo ids [14400303, 1404040, 1440583]
    repo = [int(base64.b64decode(r['node']['id'])[14:]) for r in repo]
    type = request.GET.get('type', 'both')
    post_set = _get_valid_post(type)
    count = post_set.count()
    # lst contain every valid post
    # 9 is post id and list contain its repo id [{9: [621, 1058, 325198]},...]
    lst = []
    for post in post_set:
        dic = {post.id: [], 'languages': []}
        for r in post.repo.all():
            dic[post.id].append(r.repo_id)
            dic['languages'] += [r.language] if r.language else []
        lst.append(dic)
    # Repos_len means how many repos match
    # Calculate how many point the post get
    percent_list = []
    for l in lst:
        points = (len(set(repo) & set(list(l.values())[0]))) * 1.5
        l['repos_point'] = points
        l['repos_point'] += math.log2(
            _calculate_points(list(l.values())[1], most_dict) + 1)
        percent_list.append(_sigmoid_to_percentage(l['repos_point']))
    # Calculate percentage
    sorted_percent_list = sorted(percent_list, reverse=True)
    lst = sorted(
        lst, key=itemgetter('repos_point'), reverse=True)
    # lst became [{'repos_point': 5, 9: 'repos_lst': [621, 1058, 325198]},...]
    # Post id sorted [16, 9, 10]
    # https://stackoverflow.com/questions/4916851/django-get-a-queryset-from-array-of-ids-in-specific-order
    posts_id = [list(l.keys())[0] for l in lst]
    preserved = Case(
        *[When(pk=pk, then=pos) for pos, pk in enumerate(posts_id)])
    posts = Post.objects.filter(
        id__in=posts_id).order_by(preserved)[:(count*3//3)]
    return render(
        request, 'match.html', {
            'posts': posts, 'sorted_percent_list': sorted_percent_list,
            'view': 'match', 'title': TITLE, 'type': type})
