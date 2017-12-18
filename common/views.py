from django.shortcuts import render


def index(request):
    """Front page"""
    return render(request, "index.html")

def profile(request):
    """Front page"""
    return render(request, "profile.html")
