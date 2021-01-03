from django.db import models

from account.models import User

class Search(models.Model):
    terms_en = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    websites = models.ManyToManyField("Websites")

    def __str__(self):
        return self.terms_en

class Websites(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name