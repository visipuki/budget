from django.contrib import admin
from debt.models import Debt
from debt.models import PeriodicDebt
from debt.models import StaticDebt

admin.site.register(Debt)
admin.site.register(PeriodicDebt)
admin.site.register(StaticDebt)
# Register your models here.
