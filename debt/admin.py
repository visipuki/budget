from django.contrib import admin
from debt.models import Debt
from debt.models import PeriodicDebt

admin.site.register(Debt)
admin.site.register(PeriodicDebt)
# Register your models here.
