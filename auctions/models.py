from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction_listing(models.Model):
    id = models.AutoField(primary_key = True)


class Bid(models.Model):
    id = models.AutoField(primary_key = True)


class Comment(models.Model):
    id = models.AutoField(primary_key = True)