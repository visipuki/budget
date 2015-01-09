from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from spending.models import Spending
from spending.forms import SpendingForm
from account.models import Account
from debt.models import DebtAccount
from datetime import date as d


@login_required
def spendingView(request, *args):
    user = request.user
    if request.method == 'POST':
        form = SpendingForm(request.POST)
        if form.is_valid():
            save_spending(form)
            return HttpResponseRedirect('/')
    else:
        if args:
            initial_form_values = initial_from_spending_object(args[0])
        else:
            initial_form_values = generate_initial(user)
        form = SpendingForm(initial=initial_form_values)
    l = Spending.objects.order_by('-modified')[:10]
    l = l[::-1]
    account_list = list(Account.objects.all())\
        + list(DebtAccount.objects.all())
    context = {
        'account_list': account_list,
        'latest_spending_list': l,
        'form': form,
        'username': user,
    }
    return render(
        request,
        'spending/index.html',
        context,
    )


def save_spending(form):
    incomeType = form.cleaned_data['incomeType']
    money = form.cleaned_data['money']
    Spending(
        spendingType=form.cleaned_data['spendingType'],
        money=money,
        comment=form.cleaned_data['comment'],
        date=form.cleaned_data['date'],
        owner=form.cleaned_data['owner'],
        incomeType=incomeType,
    ).save()
    change_account(incomeType, money)


def change_account(account, spending):
    a = account
    a.money -= spending
    a.save()


def initial_from_spending_object(pk):
    s = Spending.objects.get(pk=pk)
    return {
        'date':         s.date.strftime('%d-%m-%y'),
        'money':        s.money,
        'comment':      s.comment,
        'owner':        s.owner,
        'spendingType': s.spendingType,
        'incomeType':   s.incomeType
    }


def generate_initial(user):
    return {
        'date': d.today().strftime('%d-%m-%y'),
        'incomeType': Account.objects.get(
            owner=user,
            is_cost_default=True
            ),
        'owner': user
    }
