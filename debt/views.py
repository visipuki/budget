from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from spending.models import SpendingType
from debt.models import Debt, StaticDebt, PeriodicDebt, DebtAccount
from account.models import Account
from debt.forms import DebtForm
from datetime import date


@login_required
def debtView(request, *args):
    if request.method == 'POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            if args:
                update_old_debt(form, pk=args[0])
            else:
                save_new_debt(form)
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


def save_new_debt(form):
    name = form.cleaned_data['name']
    money = form.cleaned_data['money']
    owner = form.cleaned_data['owner']
    spendingType = form.cleaned_data['spendingType']
    comment = form.cleaned_data['comment']
    periodic = form.cleaned_data['periodic']

    s = StaticDebt(
        name=name,
        money=money,
        owner=owner,
        spendingType=spendingType,
        comment=comment
    )
    s.save()

    if periodic:
        p = PeriodicDebt(
            period=periodic,
            staticDebt=s,
            last_generation_date=date.today(),
        )
        p.save()
    else:
        p = None

    Debt(
        staticDebt=s,
        periodicDebt=p
    ).save()

    if not DebtAccount.objects.count():
        DebtAccount(
            id=1,
            name='Долги',
            money=0
        ).save()
    debt_account = DebtAccount.objects.get(pk=1)
    debt_account.money -= money
    debt_account.save()


def update_old_debt(form, pk):
    name = form.cleaned_data['name']
    money = form.cleaned_data['money']
    owner = form.cleaned_data['owner']
    spendingType = form.cleaned_data['spendingType']
    comment = form.cleaned_data['comment']
    periodic = form.cleaned_data['periodic']

    old_debt = Debt.objects.get(pk=pk)
    difference = money - old_debt.staticDebt.money

    s = StaticDebt(
        id=old_debt.staticDebt_id,
        name=name,
        money=money,
        owner=owner,
        spendingType=spendingType,
        comment=comment
    )
    s.save()

    if periodic:
        if old_debt.is_periodic():
            periodic_debt_id = old_debt.periodicDebt_id
        else:
            periodic_debt_id = None

        p = PeriodicDebt(
            id=periodic_debt_id,
            period=periodic,
            staticDebt=s,
            last_generation_date=date.today(),
        )
        p.save()
    else:
        p = None
        if old_debt.is_periodic():
            PeriodicDebt.objects.get(debt__id=pk).delete()

    Debt(
        id=pk,
        staticDebt=s,
        periodicDebt=p
    ).save()

    debt_account = DebtAccount.objects.get(pk=1)
    debt_account.money -= difference
    debt_account.save()


def initial_from_debt_object(pk):
    d = Debt.objects.get(pk=pk)
    s = d.staticDebt
    initial = {
        'name':         s.name,
        'money':        s.money,
        'owner':        s.owner,
        'spendingType': s.spendingType,
        'comment':      s.comment,
    }
    if d.is_periodic():
        initial['periodic'] = 'm'
    return initial


def generate_initial(user):
    initial = {
        'owner': user,
        'spendingType': SpendingType.objects.get(name='прочее'),
    }
    return initial
