from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from transfer.forms import TransferForm
from transfer.models import Transfer
from debt.models import DebtAccount
from datetime import date as d
from account.models import Account


@login_required
def transferView(request, *args):
    user = request.user
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            save_transfer(form)
            return HttpResponseRedirect('/transfer/')
    else:
        if args:
            initial_form_values = initial_from_object(args[0])
        else:
            initial_form_values = generate_initial(user)
        form = TransferForm(initial=initial_form_values)
    account_list = list(Account.objects.all())\
        + list(DebtAccount.objects.all())
    latest_transfer_list = Transfer.objects.order_by('-modified')[:10]
    context = {
        'account_list': account_list,
        'latest_transfer_list': latest_transfer_list[::-1],
        'form': form,
        'username': user
    }
    return render(
        request,
        'transfer/index.html',
        context
    )


def save_transfer(form):
        money = form.cleaned_data['money']
        source = form.cleaned_data['source']
        receiver = form.cleaned_data['receiver']
        Transfer(
            date=form.cleaned_data['date'],
            money=money,
            comment=form.cleaned_data['comment'],
            owner=form.cleaned_data['owner'],
            source=source,
            receiver=receiver,
        ).save()
        change_account(source, receiver, money)


def change_account(source, receiver, money):
    s = source
    r = receiver
    s.money -= money
    r.money += money
    s.save()
    r.save()


def initial_from_object(pk):
    # получаем начальные данные для формы из объекта
    i = Transfer.objects.get(pk=pk)
    return {
        'date':         i.date.strftime('%d-%m-%y'),
        'money':        i.money,
        'comment':      i.comment,
        'owner':        i.owner,
        'source':       i.source,
        'receiver':     i.receiver
    }


def generate_initial(user):
    # создает словарь начальных данных для формы
    return {
        'date':     d.today().strftime('%d-%m-%y'),
        'owner':    user,
        'source':   Account.objects.filter(
            owner=user,
            is_income_default=True)[0],
        'receiver': Account.objects.exclude(
            owner=user).filter(
                is_income_default=True)[0]
    }
