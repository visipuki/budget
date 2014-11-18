from django.db import models
from django.contrib.auth.models import User
from account.models import Account


class SpendingType(models.Model):
    name = models.CharField(max_length=16, unique=True)

    class Meta:
        verbose_name = 'Тип трат'
        verbose_name_plural = 'Типы трат'

    def __str__(self):
        return self.name


class Spending(models.Model):
    spendingType = models.ForeignKey(SpendingType)
    money = models.IntegerField()
    date = models.DateField()
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    comment = models.CharField(max_length=32)
    incomeType = models.ForeignKey(Account)

    def __str__(self):
        return r'{} / {} / {} / {} руб./ {}'.format(
            self.date.strftime('%d-%m-%Y'),
            self.owner,
            self.spendingType,
            self.money,
            self.comment,
        )
