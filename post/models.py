from django.db import models
from django.contrib.auth import get_user_model

class Popular(models.Model):
    globle_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256)
    name_with_owner = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank=True)
    url = models.URLField(blank=True)
    homepage_url = models.URLField(blank=True)
    primary_language = models.CharField(max_length=256, blank=True)
    star_count = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Repo(models.Model):
    repo_id = models.IntegerField()
    repo_name = models.CharField(max_length=256)
    owner_name = models.CharField(max_length=256)
    stargazers_count = models.IntegerField()
    language = models.CharField(max_length=256)
    html_url = models.URLField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner_name + '/' + self.repo_name


class Post(models.Model):
    Both = 0
    Remote = 1
    OnSite = 2

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='post')
    # job
    title = models.CharField(max_length=50)
    job_des = models.CharField(max_length=600)
    repo = models.ManyToManyField(Repo)
    onsite = models.SmallIntegerField(default=Both)
    salary = models.CharField(max_length=50)
    # company
    company_name = models.CharField(max_length=50)
    company_des = models.CharField(max_length=600)
    location = models.CharField(max_length=50)
    apply = models.CharField(max_length=256)
    pay = models.BooleanField(default=False)
    pay_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name + '---' + self.title
