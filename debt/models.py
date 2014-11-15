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
    periodicDebt = models.ForeignKey('PeriodicDebt', blank=True, null=True)

    class Meta:
        verbose_name = 'Планируемая трата'
        verbose_name_plural = 'Планируемые траты'

    def __str__(self):
        if self.is_periodic():
            periodic_flag = PeriodicDebt.objects.get(
                debt__id=self.id
            ).get_period_display()
        else:
            periodic_flag = 'разовая'
        return r'{} / {} руб. / {} / {} / {} / {}'.format(
            self.name,
            self.money,
            self.owner,
            self.spendingType,
            self.comment,
            periodic_flag
        )

    def is_periodic(self):
        return bool(self.periodicDebt)


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
    name = models.CharField(max_length=32)
    money = models.IntegerField()
    owner = models.ForeignKey(User)
    spendingType = models.ForeignKey(SpendingType)
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
