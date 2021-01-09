from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    GROUP_CHOICES = (
        (1, "Low"), 
        (2, "Mid"), 
        (3, "High")
    )

    limit = models.IntegerField(choices=GROUP_CHOICES, default=10)
