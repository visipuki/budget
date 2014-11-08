from django import forms
from django.contrib.auth.models import User
from spending.models import SpendingType


class DebtForm(forms.Form):
    name = forms.CharField(
        max_length=32, required=True,
        label='Имя планируемой траты*'
    )
    money = forms.IntegerField(
        label ='Расход*',
        required=True
    )
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label=None,
        required=False,
        label='Автор'
    )
    spendingType = forms.ModelChoiceField(
        queryset=SpendingType.objects.all(),
        required=True,
        label='Тип траты*'
    )
    comment = forms.CharField(
        max_length=32, required=False,
        label='Комментарий'
    )
    PERIOD_CHOICES = (
        (None, 'разовая трата'),
        ('m', 'ежемесячно'),
    )
    periodic = forms.ChoiceField(
        label='Периодичность',
        choices=PERIOD_CHOICES,
    )
