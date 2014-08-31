from django.db import models
from django.contrib.auth.models import User


class IncomeType(models.Model):
    name = models.CharField(max_length=16, unique=True)
    owner = models.ForeignKey(User)
    is_cost_default = models.BooleanField() #источник денег для расходов по умолчанию
    is_income_default = models.BooleanField() # источник денег для доходов по умолчанию

    def __str__(self):
        return self.name


class Income(models.Model):
    incomeType = models.ForeignKey(IncomeType)
    money = models.IntegerField()
    date = models.DateField()
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    comment = models.CharField(max_length=32)

    def __str__(self):
        return r'{} / {} / {} / {} руб.'.format(self.date.strftime('%d-%m-%Y'),
                                                self.owner,
                                                self.incomeType,
                                                self.money)
