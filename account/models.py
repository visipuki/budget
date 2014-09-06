from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    name = models.CharField(max_length=16, unique=True)
    money = models.IntegerField()
    is_cost_default = models.BooleanField()
    is_income_default = models.BooleanField()
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.name
