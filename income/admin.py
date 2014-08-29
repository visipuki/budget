from django.contrib import admin
from income.models import Income
from income.models import IncomeType

admin.site.register(Income)
admin.site.register(IncomeType)
