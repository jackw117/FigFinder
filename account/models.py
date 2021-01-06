from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import MinValueValidator, MaxValueValidator

# TODO: int current, limit groups
class User(AbstractUser):
    limit = models.IntegerField(
        choices=[(10, "Low"), (20, "Mid"), (30, "High")],
        default=10
        )
