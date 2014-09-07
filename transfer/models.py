from django.db import models
from django.contrib.auth.models import User
from account.models import Account


class Transfer(models.Model):
    date = models.DateField()
    money = models.IntegerField()
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    comment = models.CharField(max_length=32)
    source = models.ForeignKey(Account, related_name='from_account')
    receiver = models.ForeignKey(Account, related_name='to_account')

    def __str__(self):
        return r'{} / {} / {} / {} / {} руб.'.format(
            self.date.strftime('%d-%m-%Y'),
            self.owner,
            self.source,
            self.receiver,
            self.money)
