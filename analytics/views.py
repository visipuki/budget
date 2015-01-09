from django.shortcuts import render
from django.http import HttpResponseRedirect
from analytics.forms import DateRangeForm
from django.db.models import Q
from datetime import date
from datetime import datetime
from operator import itemgetter
from income.models import Income
from spending.models import Spending
from spending.models import SpendingType as Sp_t
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.models import User
from debt.models import DebtAccount
from account.models import Account


class Analysis():
    def __init__(self, name, title, data):
        self.name = name
        self.title = title
        self.data = data


@login_required
def analyticsView(request, *args):
    conditions = conditions_from(args)
    initial = initial_from(conditions)
    if request.method == 'POST':
        form = DateRangeForm(request.POST, label_suffix='')
        if form.is_valid():
            return HttpResponseRedirect(
                '/analytics/'+redirectURLtailCreation(form)
            )
    else:
        form = DateRangeForm(initial, label_suffix='')

    spending_list = Spending.objects.filter(
        dateRangeFilter(conditions),
        tagFilter(conditions, 'owner_id'),
        tagFilter(conditions, 'spendingType_id'),
        tagFilter(conditions, 'incomeType_id'),
    )
    spending_list = spending_list[::-1]
    income_list = Income.objects.filter(
        dateRangeFilter(conditions),
        tagFilter(conditions, 'owner_id'),
        tagFilter(conditions, 'incomeType_id'),
    )
    income_list = income_list[::-1]

    totals = Analysis(
        '',
        'Сумма трат по типам',
        cost_by_type(conditions)
    )
    relation = Analysis(
        '',
        'Процентное соотношение трат по типам',
        cost_relation(totals.data)
    )
    spenders = Analysis(
        '',
        'Траты по персоналиям',
        spending_by_owner(conditions)
    )
    earners = Analysis(
        '',
        'Заработки',
        earning_by_owner(conditions)
    )
    analysis_list = [
        totals,
        relation,
        spenders,
        earners,
    ]
    account_list = list(Account.objects.all())\
        + list(DebtAccount.objects.all())
    context = {
        'account_list': account_list,
        'username': request.user,
        'form': form,
        'latest_spending_list': spending_list,
        'income_list': income_list,
        'analysis_list': analysis_list,
    }
    return render(
        request,
        './analytics/index.html',
        context
    )


def cost_by_type(conditions):
    # calculates total of spended money by type of spending
    cost_list = [
        (sp_t.name, sp_t.total)
        for sp_t in Sp_t.objects.filter(
            dateRangeFilter(conditions, prefix='spending__'),
            tagFilter(conditions, 'owner_id', prefix='spending__'),
            tagFilter(conditions, 'spendingType_id', new_tag='id'),
            tagFilter(conditions, 'incomeType_id', prefix='spending__'),
        ).annotate(total=Sum('spending__money'))
    ]
    cost_list = sorted(cost_list, key=itemgetter(1), reverse=True)
    return cost_list


def cost_relation(cost_by_type):
    summ = sum([i for _, i in cost_by_type])
    if summ:
        relation = [
            (key, round(val*100/summ))
            for key, val in cost_by_type
        ]
    else:
        relation = []
    return relation


def spending_by_owner(conditions):
    return [
        (u.username, u.total)
        for u in User.objects.filter(
            tagFilter(conditions, 'owner_id', new_tag='id'),
            tagFilter(conditions, 'spendingType_id', prefix='spending__'),
            tagFilter(conditions, 'incomeType_id', prefix='spending__'),
            dateRangeFilter(conditions, prefix='spending__'),
        ).annotate(total=Sum('spending__money'))
    ]


def earning_by_owner(conditions):
    return [
        (u.username, u.total)
        for u in User.objects.filter(
            dateRangeFilter(conditions, prefix='income__'),
            tagFilter(conditions, 'owner_id', new_tag='id'),
            tagFilter(conditions, 'incomeType_id', prefix='income__'),
        ).annotate(total=Sum('income__money'))
    ]


def redirectURLtailCreation(form):
    start = form.cleaned_data['date__gte']
    end = form.cleaned_data['date__lte']
    if start > end:
        end, start = start, end
    start_str = start.strftime('%d-%m-%Y')
    end_str = end.strftime('%d-%m-%Y')
    conditions = {
        'date__gte': start_str,
        'date__lte': end_str,
        'owner_id': '_'.join([
            str(u.id)
            for u in User.objects.all()
            if form.cleaned_data[u.username]
        ]),
        'incomeType_id': '_'.join(
            str(a.id)
            for a in Account.objects.all()
            if form.cleaned_data[a.name]
        ),
        'spendingType_id': '_'.join(
            str(s.id)
            for s in Sp_t.objects.all()
            if form.cleaned_data[s.name]
        ),
    }
    redirectURLtail = ''
    for k, v in conditions.items():
        if v:
            redirectURLtail += k+'/'+v+'/'
    return redirectURLtail


def dateRangeFilter(conditions, prefix=''):
    return Q(**{
        prefix+'date__gte': datetime.strptime(
            conditions['date__gte'],
            '%d-%m-%Y'
        ),
        prefix+'date__lte': datetime.strptime(
            conditions['date__lte'],
            '%d-%m-%Y'
        )
    })


def tagFilter(conditions, tag, prefix='', new_tag=''):
    q_obj = Q()
    if tag in conditions.keys():
        id_list = conditions[tag].split('_')
        if new_tag:
            tag = new_tag
        else:
            tag = prefix + tag
        filter_expression = {}
        for id in id_list:
            filter_expression[tag] = id
            q_obj |= Q(**filter_expression)
    return q_obj


def initial_from(conditions):
    if len(conditions) == 2:
        initial = conditions
    else:
        initial = dict()
        initial['date__gte'] = conditions['date__gte']
        initial['date__lte'] = conditions['date__lte']

        spt_q_filter = tagFilter(
            conditions,
            'spendingType_id',
            new_tag='id'
        )
        if spt_q_filter:
            for s in Sp_t.objects.filter(
                spt_q_filter
            ):
                initial[s.name] = True

        income_q_filter = tagFilter(
            conditions,
            'incomeType_id',
            new_tag='id'
        )
        if income_q_filter:
            for i in Account.objects.filter(
                income_q_filter
            ):
                initial[i.name] = True

        user_q_filter = tagFilter(
            conditions,
            'owner_id',
            new_tag='id'
        )
        if user_q_filter:
            for u in User.objects.filter(
                user_q_filter
            ):
                initial[u.username] = True

    return initial


def conditions_from(view_args):
    if not view_args:
        end = date.today()
        start = end.replace(day=1)
        end_str = end.strftime('%d-%m-%Y')
        start_str = start.strftime('%d-%m-%Y')
        conditions = {
            'date__gte': start_str,
            'date__lte': end_str
        }
    else:
        args_list = list(view_args)
        del args_list[::3]
        conditions = dict(zip(args_list[::2], args_list[1::2]))
        if None in conditions.keys():
            del conditions[None]
        if conditions['date__gte'] > conditions['date__lte']:
            conditions['date__gte'], conditions['date__lte'] =\
                conditions['date__lte'], conditions['date__gte']

    return conditions
