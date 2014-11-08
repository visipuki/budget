from django import forms
from django.contrib.auth.models import User
from account.models import Account
from spending.forms import CalendarWidget


class IncomeForm(forms.Form):
    date = forms.DateField(
        label='Дата',
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
    money = forms.IntegerField(
        label ='Доход*',
    )
    comment = forms.CharField(
        max_length=32,
        required=False,
        label='комментарий'
    )
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label=None,
        required=False,
        label='автор'
    )
    incomeType = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=False,
        label='тип'
    )
