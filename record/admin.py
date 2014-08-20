from django.contrib import admin
from record.models import Spending
from record.models import SpendingType

admin.site.register(Spending)
admin.site.register(SpendingType)
