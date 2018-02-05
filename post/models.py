from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model


class Repo(models.Model):
    repo_id = models.IntegerField(unique=True)
    repo_name = models.CharField(max_length=256)
    owner_name = models.CharField(max_length=256)
    stargazers_count = models.IntegerField()
    description = models.CharField(max_length=256, blank=True, null=True)
    language = models.CharField(max_length=256, blank=True, null=True)
    url = models.URLField(blank=True)
    html_url = models.URLField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner_name + '/' + self.repo_name


class Post(models.Model):
    Both = 0
    Remote = 1
    OnSite = 2
    Yes = 1
    No = 0

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='post')
    # job
    title = models.CharField(max_length=50)
    job_des = models.CharField(max_length=4096)
    repo = models.ManyToManyField(Repo)
    type = models.SmallIntegerField(default=Both)
    visa = models.SmallIntegerField(default=No)
    salary = models.CharField(max_length=50)
    # company
    company_name = models.CharField(max_length=50)
    company_des = models.CharField(max_length=4096)
    location = models.CharField(max_length=50)
    website = models.URLField(blank=True)
    apply = models.CharField(max_length=256)
    pay = models.BooleanField(default=False)
    pay_time = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name + '---' + self.title
