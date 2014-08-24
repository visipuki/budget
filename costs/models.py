from django.db import models
from django.contrib.auth.models import User


class SpendingType(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Spending(models.Model):
    spendingType = models.ForeignKey(SpendingType)
    money = models.IntegerField()
    date = models.DateField()
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    comment = models.CharField(max_length=32)
