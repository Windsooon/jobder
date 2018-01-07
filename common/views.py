from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from post.models import Post


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
    job = get_object_or_404(Post, id=id)
    onsite = ['Both', 'Remote', 'Onsite']
    return render(
        request, 'job.html', 
        {
            'job': job, 
            'onsite': onsite[job.onsite], 
            'salary': job.salary})
