from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from income.models import Income
from income.forms import IncomeForm
from debt.models import DebtAccount
from datetime import date as d
from account.models import Account


@login_required
def incomeView(request, *args):
    user = request.user
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            save_income(form)
            return HttpResponseRedirect('/income/')
    else:
        if args:
            initial_form_values = initial_from_object(args[0])
        else:
            initial_form_values = generate_initial(user)
        form = IncomeForm(initial=initial_form_values)
    account_list = list(Account.objects.all())\
        + list(DebtAccount.objects.all())
    latest_income_list = Income.objects.order_by('-modified')[:10]
    context = {
        'account_list': account_list,
        'latest_income_list': latest_income_list[::-1],
        'form': form,
        'username': user
    }
    return render(
        request,
        './income/index.html',
        context
    )


def save_income(form):
    money = form.cleaned_data['money']
    incomeType = form.cleaned_data['incomeType']
    Income(
        date=form.cleaned_data['date'],
        money=money,
        comment=form.cleaned_data['comment'],
        owner=form.cleaned_data['owner'],
        incomeType=incomeType
    ).save()
    change_account(incomeType, money)


def change_account(account, income):
    a = account
    a.money += income
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
        'incomeType':   Account.objects.filter(
            owner=user,
            is_income_default=True
            )[0]
    }
