import os
from django.core import serializers
from django.contrib.auth.models import User
from account.models import Account
from spending.models import SpendingType

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_xml_fixtures():
    query_set_list = list(User.objects.all()) + list(Account.objects.all()) + list(SpendingType.objects.all())
    with open(
        os.path.join(
            BASE_DIR,
            'initial_data.xml'), 'w') as out:
        data = serializers.serialize("xml", query_set_list)
        out.write(data)
