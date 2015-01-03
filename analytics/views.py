from django.shortcuts import render
from django.http import HttpResponseRedirect
from analytics.forms import DateRangeForm
from datetime import date
from datetime import datetime
from operator import itemgetter
from spending.models import Spending
from spending.models import SpendingType as Sp_t
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


class Analysis():
    def __init__(self, name, title, data):
        self.name = name
        self.title = title
        self.data = data


@login_required
def analyticsView(request, *args):
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['startDate']
            end = form.cleaned_data['endDate']
            if start > end:
                end, start = start, end
            start_str = start.strftime('%d-%m-%Y')
            end_str = end.strftime('%d-%m-%Y')
            return HttpResponseRedirect(
                '/analytics/'+start_str+'_'+end_str+'/'
            )
    else:
        if not args:
            end = date.today()
            start = end.replace(day=1)
            end_str = end.strftime('%d-%m-%Y')
            start_str = start.strftime('%d-%m-%Y')
        else:
            start_str, end_str = args[0], args[1]
            start = datetime.strptime(start_str, '%d-%m-%Y')
            end = datetime.strptime(end_str, '%d-%m-%Y')
            if start > end:
                end, start = start, end
                end_str, start_str = start_str, end_str
        form = DateRangeForm(initial={'startDate': start_str,
                                      'endDate': end_str})

    l = Spending.objects.filter(date__lte=end).filter(date__gte=start)
    l = l[::-1]
    totals = Analysis(
        'totals',
        'Сумма трат по типам за указанный период',
        cost_by_type(start, end)
    )
    relation = Analysis(
        'relation',
        'Процентное соотношение трат по типам за указанный период',
        cost_relation(totals.data)
    )

    analysis_list = [totals, relation]
    context = {'username': request.user,
               'form': form,
               'latest_spending_list': l,
               'analysis_list': analysis_list}
    return render(request,
                  './analytics/index.html',
                  context)


def cost_by_type(start, end):
    # calculates total of spended money by type of spending
    cost_list = [
        (sp_t.name, sp_t.total)
        for sp_t in Sp_t.objects.filter(
            spending__date__gte=start,
            spending__date__lte=end
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
