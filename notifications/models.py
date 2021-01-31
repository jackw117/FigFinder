from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

from account.models import User

class Websites(models.Model):
    base_url = models.URLField()
    url = models.URLField()
    url_right = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=25)
    className = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Search(models.Model):
    terms_en = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    websites = models.ManyToManyField(Websites, through="Details")

    def __str__(self):
        return self.terms_en

class Entry(models.Model):
    name = models.CharField(max_length=150)
    url = models.URLField()
    new = models.BooleanField(default=False)

class Details(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    website = models.ForeignKey(Websites, on_delete=models.CASCADE)
    # details = ArrayField(
    #     models.ForeignKey(Entry, on_delete=models.CASCADE),
    #     null=True,
    #     blank=True
    # )
    details = models.ManyToManyField(Entry)
    time = models.DateTimeField(auto_now=True)

