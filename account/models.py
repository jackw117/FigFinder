from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator

# TODO: custom user with search limits
class User(AbstractUser):
    limit = models.IntegerField(validators=[MaxValueValidator(10)])
