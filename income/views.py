from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from income.models import Income
from income.forms import IncomeForm
from datetime import date as d


@login_required
def incomeView(request, *args):
    if request.method == 'POST':
        save_income(request)
        return HttpResponseRedirect('/income/')
    else:
        user = request.user
        if args:
            initial_form_values = initial_from_object(args[0])
        else:
            initial_form_values = generate_initial(user)
        form = IncomeForm(initial=initial_form_values)
        l = Income.objects.order_by('-modified')[:5]
        latest_income_list = l[::-1]
        context = {
            'latest_income_list': latest_income_list,
            'form': form,
            'username': user
        }
        return render(
            request,
            'income/index.html',
            context
        )


def save_income(request):
    form = IncomeForm(request.POST)
    if form.is_valid():
        date = form.cleaned_data['date']
        money = form.cleaned_data['money']
        comment = form.cleaned_data['comment']
        incomeType = form.cleaned_data['incomeType']
        is_cash = form.cleaned_data['is_cash']
        owner = form.cleaned_data['owner']
        Income(
            incomeType=incomeType,
            money=money,
            comment=comment,
            date=date,
            owner=owner
        ).save()


def initial_from_object(pk):
    i = Income.objects.get(pk)
    return {
        'date':         i.date.strftime('%d-%m-%y'),
        'money':        i.money,
        'comment':      i.comment,
        'owner':        i.owner,
        'incomeType':   i.incomeType,
    }


def generate_initial(user):
    return {
        'date':         d.today().strftime('%d-%m-%y'),
        'owner':        user
        'incomeType':   IncomeType.objects.filter(
            incometype__owner__eq=user,
            incometype__is_default=True
            ).name,
    }

