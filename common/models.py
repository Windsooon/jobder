from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import allauth
from post.models import Repo


class Settings(models.Model):
    Both = 0
    Remote = 1
    OnSite = 2

    user = models.OneToOneField(
        allauth.app_settings.USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='settings',
    )
    blog = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    visiable = models.BooleanField(default=True)
    type = models.SmallIntegerField(default=Both)
    repo = models.ManyToManyField(Repo)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    settings = models.ForeignKey(
        Settings,
        on_delete=models.CASCADE,
        related_name='customer',
        blank=True, null=True)
    cus_id = models.CharField(max_length=256, blank=True)
    post_id = models.IntegerField(blank=True, null=True)
    sub_id = models.CharField(max_length=256, blank=True)
    stripe_name = models.CharField(max_length=256, blank=True)
    stripe_email = models.EmailField(blank=True)
    stripe_zip = models.CharField(max_length=256, blank=True)
    stripe_last4 = models.CharField(max_length=48, blank=True)
    stripe_exp_month = models.SmallIntegerField(blank=True, null=True)
    stripe_exp_year = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.cus_id


class FakeUser(models.Model):
    username = models.CharField(max_length=256, blank=True)
    avatar_url = models.CharField(max_length=256, blank=True)
    repo = models.ManyToManyField(Repo)

    def __str__(self):
        return self.username


@receiver(post_save, sender=allauth.app_settings.USER_MODEL)
def init_settings(sender, instance, **kwargs):
    Settings.objects.update_or_create(
        user_id=instance.id,
    )
