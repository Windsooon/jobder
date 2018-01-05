from django.db import models


class Repo(models.Model):
    name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Post(models.Model):
    Both = 0
    Remote = 1
    OnSite = 2

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
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name + '---' + self.title
