from django.db import models
from django.spending.models import SpendingType
from django.contrib.auth.models import User


class Debt(models.Model):
    name = models.CharField(max_length=32)
    money = models.IntegerField()
    owner = models.ForeignKey(User)
    spendingType = models.ForeignKey(SpendingType)
    comment = models.CharField(max_length=32)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return r'{} / {} / {} / {} руб. / {}'.format(
            self.name,
            self.owner,
            self.spendingType,
            self.money,
            self.comment,
        )


class PeriodicalDebt(models.Model):
    PERIOD_CHOICES = (
        ('y', 'Год'),
        ('m', 'Месяц'),
        ('w', 'Неделя'),
        ('d', 'День'),
    )
    period = models.CharField(
        max_length=1,
        choices=PERIOD_CHOICES,
        default='m'
    )
    name = models.CharField(max_length=32)
    money = models.IntegerField()
    owner = models.ForeignKey(User)
    spendingType = models.ForeignKey(SpendingType)
    last_generation_date = models.DateField()

    class Meta:
        verbose_name = 'Автоматический долг'
        verbose_name_plural = 'Автоматические долги'
