from django.db import models

# Create your models here.
class SpendingType(models.Model):
    name = models.CharField(max_length=16)

class Spending(models.Model):
    spendingType = models.ForeignKey(SpendingType)
    money = models.DecimalField(max_digits=4,decimal_places=2)
    data = models.DateField()
