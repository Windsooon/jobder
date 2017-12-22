from django.shortcuts import render


def index(request):
    """Front page"""
    return render(request, "index.html")


def profile(request):
    """Profile page"""
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
