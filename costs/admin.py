from django.contrib import admin
from costs.models import Spending
from costs.models import SpendingType

admin.site.register(Spending)
admin.site.register(SpendingType)