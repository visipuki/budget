from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from costs.models import Spending
from costs.forms import SpendingForm
from datetime import date as d


@login_required
def spendingView(request):
    if request.method == 'POST':
        form = SpendingForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            money = form.cleaned_data['money']
            comment = form.cleaned_data['comment']
            spendingType = form.cleaned_data['spendingType']
            is_cash = form.cleaned_data['is_cash']
            owner = form.cleaned_data['owner']
            if not owner: owner = request.user
            Spending(spendingType=spendingType,
                     money=money,
                     comment=comment,
                     date=date,
                     owner=owner,
                     is_cash=is_cash).save()
            return HttpResponseRedirect('/')
    else:
        form = SpendingForm(initial={'date': d.today().strftime('%d-%m-%y'),
                                     'is_cash': True})
    l = Spending.objects.order_by('-modified')[:5]
    latest_spending_list = l[::-1]
    context = {'latest_spending_list': latest_spending_list,
               'form': form,
               'username': request.user}
    return render(request,
                  'costs/index.html',
                  context)
