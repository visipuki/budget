from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from income.models import Income
from income.forms import IncomeForm
from income.models import IncomeType
from datetime import date as d
from account.models import Account


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
        latest_income_list = Income.objects.order_by('-modified')[:5]
        context = {
            'latest_income_list': latest_income_list[::-1],
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
        owner = form.cleaned_data['owner']
        incomeType = form.cleaned_data['incomeType']
        Income(
            date=date,
            money=money,
            comment=comment,
            owner=owner,
            incomeType=incomeType
        ).save()
        change_account(incomeType, money)


def change_account(incomeType, spending):
    if not Account.objects.filter(accountType=incomeType):
        a = Account(accountType=incomeType, money = -spending)
    else:
        a = Account.objects.get(accountType=incomeType)
        a.money -= spending
    a.save()


def initial_from_object(pk):
    # получаем начальные данные для формы из объекта
    i = Income.objects.get(pk=pk)
    return {
        'date':         i.date.strftime('%d-%m-%y'),
        'money':        i.money,
        'comment':      i.comment,
        'owner':        i.owner,
        'incomeType':   i.incomeType,
    }


def generate_initial(user):
    # создает словарь начальных данных для формы
    return {
        'date':         d.today().strftime('%d-%m-%y'),
        'owner':        user,
        'incomeType':   IncomeType.objects.filter(
            owner=user,
            is_income_default=True
            )[0]
    }
