from django.db import models
from spending.models import SpendingType
from django.contrib.auth.models import User


class Debt(models.Model):
    staticDebt = models.ForeignKey('StaticDebt')
    periodicDebt = models.ForeignKey('PeriodicDebt', blank=True, null=True)

    def __str__(self):
        return r'{} / {} руб. / {} / {} / {}'.format(
            self.staticDebt.name,
            self.staticDebt.money,
            self.staticDebt.owner,
            self.staticDebt.spendingType,
            self.staticDebt.comment,

        )

    def is_periodic(self):
        return bool(self.periodicDebt)


class StaticDebt(models.Model):
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

    def is_periodic(self):
        return bool(self.periodicDebt)


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
    last_generation_date = models.DateField()

    class Meta:
        verbose_name = 'Периодическая трата'
        verbose_name_plural = 'Периодические траты'

    def __str__(self):
        return r'{} / {} руб. / {} / {} / {}'.format(
            self.name,
            self.money,
            self.owner,
            self.spendingType,
            self.last_generation_date,
        )


class DebtAccount(models.Model):
    name = models.CharField(max_length=32)
    money = models.IntegerField()
