from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


def index(request):
    """Front page"""
    return render(request, "index.html")


def profile(request, name):
    """Profile page"""
    user = get_object_or_404(get_user_model(), username=name)
    return render(request, "profile.html")


def settings(request):
    """Settings page"""
    if request.user.is_authenticated:
        return render(request, "settings.html")
    else:
        return render(request, "404.html")


def post_job(request):
    """Post job page"""
    return render(request, "post_job.html")
