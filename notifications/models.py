from django.db import models

class Search(models.Model):
    terms = models.CharField(max_length=200)