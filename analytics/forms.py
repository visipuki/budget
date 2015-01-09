from django import forms
from spending.models import SpendingType
from spending.forms import CalendarWidget
from django.contrib.auth.models import User
from account.models import Account


class DateRangeForm(forms.Form):
    date__gte = forms.DateField(
        required=True,
        label='с',
        input_formats=[
            '%d-%m-%Y',
            '%d-%m-%y',
            '%d/%m/%y',
            '%d/%m/%Y',
            '%d.%m.%y',
            '%d.%m.%Y'
        ],
        widget=CalendarWidget()
    )
    date__lte = forms.DateField(
        required=True,
        label='по',
        input_formats=[
            '%d-%m-%Y',
            '%d-%m-%y',
            '%d/%m/%y',
            '%d/%m/%Y',
            '%d.%m.%y',
            '%d.%m.%Y'
        ],
        widget=CalendarWidget()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for u in User.objects.all():
            self.fields[u.username] = forms.BooleanField(
                required=False,
            )
        for a in Account.objects.all():
            self.fields[a.name] = forms.BooleanField(
                required=False,
            )
        for s in SpendingType.objects.all():
            self.fields[s.name] = forms.BooleanField(
                required=False,
            )

    def userTag_fields(self):
        return [
            field for field in self
            if field.name in [u.username for u in User.objects.all()]
        ]

    def accountTag_fields(self):
        return [
            field for field in self
            if field.name in [u.name for u in Account.objects.all()]
        ]

    def spendingTypeTag_fields(self):
        return [
            field for field in self
            if field.name in [u.name for u in SpendingType.objects.all()]
        ]

    def dateTag_fields(self):
        return [
            field for field in self
            if field.name == 'date__lte' or
            field.name == 'date__gte'
        ]
