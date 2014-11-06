from django import forms
from django.contrib.auth.models import User
from account.models import Account
from spending.forms import CalendarWidget


class TransferForm(forms.Form):
    date = forms.DateField(required=True,
                           label='Дата',
                           input_formats=['%d-%m-%Y',
                                          '%d-%m-%y',
                                          '%d/%m/%y',
                                          '%d/%m/%Y',
                                          '%d.%m.%y',
                                          '%d.%m.%Y'],
                           widget=CalendarWidget())
    money = forms.IntegerField(
        label ='Сумма*',
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
    source = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=True,
        label='счет отправителя'
    )
    receiver = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=True,
        label='счет получателя'
    )
