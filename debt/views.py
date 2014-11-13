from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from spending.models import SpendingType
from debt.models import Debt, PeriodicDebt, DebtAccount
from account.models import Account
from debt.forms import DebtForm
from datetime import date as d


@login_required
def debtView(request, *args):
    if request.method == 'POST':
        if args:
            update_old_debt(request, pk=args[0])
        else:
            save_new_debt(request)
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
        account_list = list(Account.objects.all())\
            + list(DebtAccount.objects.all())
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


def save_new_debt(request):
    form = DebtForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        money = form.cleaned_data['money']
        owner = form.cleaned_data['owner']
        spendingType = form.cleaned_data['spendingType']
        comment = form.cleaned_data['comment']
        periodic = form.cleaned_data['periodic']

        if periodic:
            p = PeriodicDebt(
                period=periodic,
                name=name,
                money=money,
                owner=owner,
                spendingType=spendingType,
                last_generation_date=d.today(),
            )
            p.save()
            Debt(
                name=name,
                money=money,
                owner=owner,
                spendingType=spendingType,
                comment=comment,
                periodicDebt=p
            ).save()
        else:
            Debt(
                name=name,
                money=money,
                owner=owner,
                spendingType=spendingType,
                comment=comment,
            ).save()

        if not DebtAccount.objects.count():
            DebtAccount(
                id=1,
                name='Долги',
                money=0
            ).save()
        total = DebtAccount.objects.get(pk=1).money
        total -= money
        DebtAccount(
            id=1,
            name='Долги',
            money=total
        ).save()


def update_old_debt(request, pk):
    form = DebtForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        money = form.cleaned_data['money']
        owner = form.cleaned_data['owner']
        spendingType = form.cleaned_data['spendingType']
        comment = form.cleaned_data['comment']
        periodic = form.cleaned_data['periodic']

        difference = money - Debt.objects.get(pk=pk).money

        if periodic:
            p = PeriodicDebt(
                id = PeriodicDebt.objects.get(debt__periodicDebt=pk).id,
                period=periodic,
                name=name,
                money=money,
                owner=owner,
                spendingType=spendingType,
                last_generation_date=d.today(),
            )
            p.save()
            Debt(
                id=pk,
                name=name,
                money=money,
                owner=owner,
                spendingType=spendingType,
                comment=comment,
                periodicDebt=p
            ).save()
        else:
            Debt(
                id=pk,
                name=name,
                money=money,
                owner=owner,
                spendingType=spendingType,
                comment=comment,
            ).save()

        total = DebtAccount.objects.get(pk=1).money
        total -= difference
        DebtAccount(
            id=1,
            name='Долги',
            money=total
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
    if not i.periodicDebt:
        initial['periodic'] = 'm'
    return initial


def generate_initial(user):
    initial = {
        'owner': user,
        'spendingType': SpendingType.objects.get(name='прочее'),
    }
    return initial
