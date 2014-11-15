from django.shortcuts import render
from django.http import HttpResponseRedirect
from analytics.forms import DateRangeForm
from datetime import date
from datetime import datetime
from calendar import monthrange
from operator import itemgetter
from spending.models import SpendingType as Sp_t
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


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
            if end.day == monthrange(end.year, end.month)[1]:
                start = end.replace(day=1)
            elif end.day+1 > monthrange(end.year, end.month-1)[1]:
                start = end.replace(day=1)
            else:
                start = end.replace(month=end.month-1, day=end.day+1)
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
    totals = cost_by_type(start, end)
    relation = cost_relation(totals)

    context = {'username': request.user,
               'form': form,
               'totals': totals,
               'relation': relation}
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
