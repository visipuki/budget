from django.db import models
from income.models import IncomeType


class Account(models.Model):
    money = models.IntegerField()
    accountType = models.ForeignKey(IncomeType)
