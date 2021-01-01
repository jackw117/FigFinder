from django.db import models

class Search(models.Model):
    terms_en = models.CharField(max_length=50)
    terms_jp = models.CharField(max_length=50)
    user_id = models.IntegerField()
    websites = models.ManyToManyField("Websites")

class Websites(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name