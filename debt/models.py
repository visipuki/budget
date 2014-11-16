from django.db import models
from spending.models import SpendingType
from django.contrib.auth.models import User


class Debt(models.Model):
    staticDebt = models.ForeignKey('StaticDebt')
    periodicDebt = models.ForeignKey('PeriodicDebt', blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_periodic():
            periodic_flag = self.periodicDebt.get_period_display()
        else:
            periodic_flag = 'разовая'
        return r'{} / {}'.format(
            self.staticDebt,
            periodic_flag,
        )

    def is_periodic(self):
        return bool(self.periodicDebt)

    class Meta:

        verbose_name = 'Планируемая трата'
        verbose_name_plural = 'Планируемые траты'


class StaticDebt(models.Model):
    name = models.CharField(max_length=32)
    money = models.IntegerField()
    owner = models.ForeignKey(User)
    spendingType = models.ForeignKey(SpendingType)
    comment = models.CharField(max_length=32)

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
        ('y', 'раз в год'),
        ('m', 'раз в месяц'),
        ('w', 'раз в неделю'),
        ('d', 'раз в день'),
    )
    period = models.CharField(
        max_length=1,
        choices=PERIOD_CHOICES,
        default='m'
    )
    staticDebt = models.OneToOneField('StaticDebt')
    last_generation_date = models.DateField()

    class Meta:
        verbose_name = 'Периодическая трата'
        verbose_name_plural = 'Периодические траты'

    def __str__(self):
        return r'{} / {} / {}'.format(
            self.staticDebt,
            self.period,
            self.last_generation_date,
        )


class DebtAccount(models.Model):
    name = models.CharField(max_length=32)
    money = models.IntegerField()
