from django.db import models
from spending.models import SpendingType
from django.contrib.auth.models import User


class Debt(models.Model):
    name = models.CharField(max_length=32)
    money = models.IntegerField()
    owner = models.ForeignKey(User)
    spendingType = models.ForeignKey(SpendingType)
    comment = models.CharField(max_length=32)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Планируемая трата'
        verbose_name_plural = 'Планируемые траты'

    def __str__(self):
        return r'{} / {} руб. / {} / {} / {}'.format(
            self.name,
            self.money,
            self.owner,
            self.spendingType,
            self.comment,
        )


class PeriodicDebt(models.Model):
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
        verbose_name = 'Автоматическая трата'
        verbose_name_plural = 'Автоматические траты'

    def __str__(self):
        return r'{} / {} руб. / {} / {} / {}'.format(
            self.name,
            self.money,
            self.owner,
            self.spendingType,
            self.last_generation_date,
        )
