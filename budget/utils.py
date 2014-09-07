import os
from django.core import serializers
from django.contrib.auth.models import User
from account.models import Account
from spending.models import SpendingType

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_xml_fixtures():
    XMLSerializer = serializers.get_serializer("xml")
    xml_serializer = XMLSerializer()
    query_set_list = [
        User.objects.all(),
        Account.objects.all(),
        SpendingType.objects.all()]
    with open(
        os.path.join(
            BASE_DIR,
            'initial_data.xml'), 'w') as out:
        for q in query_set_list:
            xml_serializer.serialize(q, stream=out)


def get_json_fixtures():
    JSONSerializer = serializers.get_serializer("json")
    json_serializer = JSONSerializer()
    query_set_list = [
        User.objects.all(),
        Account.objects.all(),
        SpendingType.objects.all()]
    with open(
        os.path.join(
            BASE_DIR,
            'initial_data.json'), 'w') as out:
        for q in query_set_list:
            json_serializer.serialize(q, stream=out)
