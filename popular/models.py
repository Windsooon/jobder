from django.db import models


class Popular(models.Model):
    globle_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256)
    name_with_owner = models.CharField(max_length=256)
    description = models.CharField(max_length=256, default="", null=True)
    url = models.URLField(default="")
    homepage_url = models.URLField(default="", null=True)
    primary_language = models.CharField(max_length=256, default="", null=True)
    star_count = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
