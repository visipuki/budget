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
    if request.method == 'POST':
        save_spending(request)
        return HttpResponseRedirect('/')
    else:
        user = request.user
        if args:
            initial_form_values = initial_from_spending_object(args[0])
        else:
            initial_form_values = generate_initial(user)
        form = SpendingForm(initial=initial_form_values)
        l = Spending.objects.order_by('-modified')[:5]
        l = l[::-1]
        account_list = list(Account.objects.all())\
            + list(DebtAccount.objects.all())
        context = {
            'account_list': account_list,
            'latest_spending_list': l,
            'form': form,
            'username': user}
        return render(request,
                      'spending/index.html',
                      context)


def save_spending(request):
    form = SpendingForm(request.POST)
    if form.is_valid():
        date = form.cleaned_data['date']
        money = form.cleaned_data['money']
        comment = form.cleaned_data['comment']
        spendingType = form.cleaned_data['spendingType']
        incomeType = form.cleaned_data['incomeType']
        owner = form.cleaned_data['owner']
        Spending(spendingType=spendingType,
                 money=money,
                 comment=comment,
                 date=date,
                 owner=owner,
                 incomeType=incomeType
                 ).save()
        change_account(incomeType, money)


def change_account(account, spending):
    a = account
    a.money -= spending
    a.save()


def initial_from_spending_object(pk):
    i = Spending.objects.get(pk=pk)
    initial = {
        'date':         i.date.strftime('%d-%m-%y'),
        'money':        i.money,
        'comment':      i.comment,
        'owner':        i.owner,
        'spendingType': i.spendingType,
        'incomeType':   i.incomeType
    }
    return initial


def generate_initial(user):
    initial = {
        'date':         d.today().strftime('%d-%m-%y'),
        'incomeType':   Account.objects.filter(
            owner=user,
            is_cost_default=True
            )[0],
        'owner':        user
    }
    return initial
