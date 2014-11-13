from django import forms
from django.contrib.auth.models import User
from spending.models import SpendingType


class DebtForm(forms.Form):
    name = forms.CharField(
        max_length=32,
        label='Имя планируемой траты*'
    )
    money = forms.IntegerField(
        label ='сумма*',
        min_value = 1
    )
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label=None,
        required=False,
        label='Автор'
    )
    spendingType = forms.ModelChoiceField(
        queryset=SpendingType.objects.all(),
        empty_label=None,
        required=False,
        label='Тип траты'
    )
    comment = forms.CharField(
        max_length=32,
        required=False,
        label='Комментарий'
    )
    PERIOD_CHOICES = (
        ('', 'разовая трата'),
        ('m', 'ежемесячная трата'),
    )
    periodic = forms.ChoiceField(
        label='Периодичность',
        choices=PERIOD_CHOICES,
        required=False,
    )
