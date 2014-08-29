from django.db import models
from django.contrib.auth.models import User


class AccountType(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Account(models.Model):
    owner = models.ForeignKey(User)
    money = models.IntegerField()
    accountType = models.ForeignKey(AccountType)
    is_cashe = models.BooleanField()
