from django import forms
from spending.models import SpendingType
from spending.forms import CalendarWidget


class DateRangeForm(forms.Form):
    startDate = forms.DateField(required=True,
                                label='с',
                                input_formats=['%d-%m-%Y',
                                               '%d-%m-%y',
                                               '%d/%m/%y',
                                               '%d/%m/%Y',
                                               '%d.%m.%y',
                                               '%d.%m.%Y'],
                                widget=CalendarWidget())
    endDate = forms.DateField(required=True,
                                label='по',
                                input_formats=['%d-%m-%Y',
                                               '%d-%m-%y',
                                               '%d/%m/%y',
                                               '%d/%m/%Y',
                                               '%d.%m.%y',
                                               '%d.%m.%Y'],
                                widget=CalendarWidget())
