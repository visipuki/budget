from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from income.models import Income
from income.forms import IncomeForm
from datetime import date as d


@login_required
def incomeView(request):
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
            return HttpResponseRedirect('/')
    else:
        form = IncomeForm(initial={'date': d.today().strftime('%d-%m-%y'),
                                   'is_cash': True})
    l = Income.objects.order_by('-modified')[:5]
    latest_income_list = l[::-1]
    context = {'latest_income_list': latest_income_list,
               'form': form,
               'username': request.user}
    return render(request,
                  'costs/index.html',
                  context)
