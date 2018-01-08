import datetime
import logging
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from post.models import Post
from jobs.set_logging import setup_logging

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

    logger.debug('just base debug')
    logger.info('just base info')

    try:
        job = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return render(request, '404.html')
    else:
        # not pay yet or expired
        if not job.pay or ((datetime.datetime.now() -
            datetime.timedelta(days=30)) > job.pay_time):
            if request.user != job.user:
                return render(request, '404.html')
    return render(
        request, 'job.html',
        {
            'job': job,
            'onsite': onsite[job.onsite],
            'salary': job.salary})
