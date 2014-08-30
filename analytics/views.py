from django.shortcuts import render
from django.http import HttpResponseRedirect
from analytics.forms import DateRangeForm
from datetime import date
from datetime import datetime
from costs.models import Spending, SpendingType
from django.contrib.auth.decorators import login_required


@login_required
def analyticsView(request, *args):
    if not args:
        end = date.today()
        start = end.replace(month=end.month-1)
        end_str = end.strftime('%d-%m-%Y')
        start_str = start.strftime('%d-%m-%Y')
    else:
        start_str, end_str = args[0], args[1]
        start = datetime.strptime(start_str, '%d-%m-%Y')
        end = datetime.strptime(end_str, '%d-%m-%Y')
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['startDate']
            end = form.cleaned_data['endDate']
            start_str = start.strftime('%d-%m-%Y')
            end_str = end.strftime('%d-%m-%Y')
            return HttpResponseRedirect('/analytics/'+start_str+'_'+end_str+'/')
    else:
        form = DateRangeForm(initial={'startDate': start_str,
                                      'endDate': end_str})
    relation = spending_percentage_relation(start, end)
    context = {'username': request.user,
               'form': form,
               'relation': relation}
    return render(request,
                  './analytics/index.html',
                  context)


def spending_percentage_relation(start, end):
    # calculates percentage relation of all spendings grouped by its type
    # per specified period
    spendingList = Spending.objects.filter(date__gte=start,
                                           date__lte=end)
    summ = 0 #добавить условие для 0
    relation = {spendingType.name: 0 for spendingType in SpendingType.objects.all()}
    for i in spendingList:
        summ += i.money
        relation[str(i.spendingType)] += i.money
    for t, s in relation.items():
        relation[t] = int(round(relation[t]*100/float(summ)))
    return relation
