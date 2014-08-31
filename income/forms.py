from django import forms
from django.contrib.auth.models import User
from income.models import IncomeType


class IncomeForm(forms.Form):
    date = forms.DateField(
        required=True,
        label='Дата',
        input_formats=[
            '%d-%m-%Y',
            '%d-%m-%y',
            '%d/%m/%y',
            '%d/%m/%Y',
            '%d.%m.%y',
            '%d.%m.%Y'
        ]
    )
    money = forms.IntegerField(
        label ='Доход*',
        required=True
    )
    comment = forms.CharField(
        max_length=32, required=False,
        label='комментарий'
    )
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label=None,
        required=False,
        label='автор'
    )
    incomeType = forms.ModelChoiceField(
        queryset=IncomeType.objects.all(),
        required=True,
        label='тип*'
    )
