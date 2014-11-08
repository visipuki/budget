from django.db import models
from django.spending.models import SpendingType
from django.contrib.auth.models import User


class Debt(models.Model):
    spendingType = models.ForeignKey(SpendingType)
    money = models.IntegerField()
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=32)
    comment = models.CharField(max_length=32)

    def __str__(self):
        return r'{} / {} / {} / {} руб. / {}'.format(
            self.name,
            self.owner,
            self.spendingType,
            self.money,
            self.comment
        )


class PeriodicalDebt(models.Model):
    PERIOD_choices = (
        ('y', 'Год'),
        ('m', 'Месяц'),
        ('w', 'Неделя'),
        ('d', 'День'),
    )
    period = models.CharField(
        max_length=1,
        choices=PERIOD_choices,
        defaul='m'
    )
    spendingType = models.ForeignKey(SpendingType)
    money = models.IntegerField()
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(User)

    class Meta:
        verbose_name = 'Автоматический долг'
        verbose_name_plural = 'Автоматические долги'

