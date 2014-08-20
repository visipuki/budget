from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from record.models import Spending


@login_required
def spendingView(request):
    latest_spending_list = Spending.objects.order_by('-data')[:5]
    context = {'latest_spending_list': latest_spending_list}
    return render(request, 'record/index.html', context)
