from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from debt.models import Debt, PeriodicalDebt
from account.models import Account
from debt.forms import DebtForm
from datetime import date as d


@login_required
def debtView(request, *args):
    if request.method == 'POST':
        save_debt(request)
        return HttpResponseRedirect('/debt/')
    else:
        user = request.user
        if args:
            initial_form_values = initial_from_debt_object(args[0])
        else:
            initial_form_values = generate_initial(user)
        form = DebtForm(initial=initial_form_values)
        l = Debt.objects.order_by('-modified')
        l = l[::-1]
        account_list = Account.objects.all()
        context = {
            'account_list': account_list,
            'debt_list': l,
            'form': form,
            'username': user
        }
        return render(
            request,
            'debt/index.html',
            context
        )


def save_debt(request):
    form = DebtForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        money = form.cleaned_data['money']
        owner = form.cleaned_data['owner']
        spendingType = form.cleaned_data['spendingType']
        comment = form.cleaned_data['comment']
        periodic = form.cleaned_data['periodic']
        Debt(
            name=name,
            money=money,
            owner=owner,
            spendingType=spendingType,
            comment=comment,
        ).save()
        if periodic:
            PeriodicalDebt(
                name=name,
                money=money,
                owner=owner,
                spendingType=spendingType,
                last_generation_date=d.today(),
                period=periodic,
            ).save()


def initial_from_debt_object(pk):
    i = Debt.objects.get(pk=pk)
    initial = {
        'name':         i.name,
        'money':        i.money,
        'owner':        i.owner,
        'spendingType': i.spendingType,
        'comment':      i.comment,
    }
    return initial


def generate_initial(user):
    initial = {
        'owner': user
    }
    return initial
