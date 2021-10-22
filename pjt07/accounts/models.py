from typing import AbstractSet
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followings')