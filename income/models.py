from django.db import models
from django.contrib.auth.models import User
from account.models import Account


class Income(models.Model):
    incomeType = models.ForeignKey(Account)
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
