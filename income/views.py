from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from income.models import Income
from income.forms import IncomeForm
from datetime import date as d


@login_required
def incomeView(request, *args):
    if args:
        i = Income.objects.get(pk=args[0])
        initial_form_values = {'date': i.date.strftime('%d-%m-%y'),
                               'money': i.money,
                               'comment': i.comment,
                               'owner': i.owner,
                               'incomeType': i.incomeType,
                               'is_cash': i.is_cash}
    else:
        initial_form_values = {'date': d.today().strftime('%d-%m-%y'),
                               'is_cash': True}
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            money = form.cleaned_data['money']
            comment = form.cleaned_data['comment']
            incomeType = form.cleaned_data['incomeType']
            is_cash = form.cleaned_data['is_cash']
            owner = form.cleaned_data['owner']
            if not owner:
                owner = request.user
            Income(incomeType=incomeType,
                   money=money,
                   comment=comment,
                   date=date,
                   owner=owner,
                   is_cash=is_cash).save()
            return HttpResponseRedirect('/income/')
    else:
        form = IncomeForm(initial=initial_form_values)
    l = Income.objects.order_by('-modified')[:5]
    latest_income_list = l[::-1]
    context = {'latest_income_list': latest_income_list,
               'form': form,
               'username': request.user}
    return render(request,
                  'income/index.html',
                  context)
