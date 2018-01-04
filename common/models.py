from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import allauth


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
    onsite = models.SmallIntegerField(default=Both)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user__username


@receiver(post_save, sender=allauth.app_settings.USER_MODEL)
def init_settings(sender, instance, **kwargs):
    Settings.objects.update_or_create(
        user_id=instance.id,
    )
