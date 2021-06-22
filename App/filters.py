import django_filters
from .models import *
from django import forms


class TImeActivityFilter(django_filters.FilterSet):
    class Meta:
        model = TimeActivity
        fields = ['employee' , 'item']

        widgets = {
            'employee' : forms.Select(attrs={
                'class' : 'form-select'
            }),
        }