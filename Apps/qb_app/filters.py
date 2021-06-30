import django_filters
from .models import *


class TImeActivityFilter(django_filters.FilterSet):
    class Meta:
        model = TimeActivity
        fields = ['employee', 'item']
