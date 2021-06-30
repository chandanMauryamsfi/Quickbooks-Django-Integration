from django import forms
from django.forms import ModelForm

from Apps.qb_app.models import Employee, Item, PrimaryAddr, TimeActivity


class EmployeeForm(ModelForm):

    class Meta:
        model = Employee
        fields = ['given_Name', 'family_Name']

        widgets = {
            'given_Name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'family_Name': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }


class PrimaryAddrForm(ModelForm):
    class Meta:
        model = PrimaryAddr
        fields = ['city', 'postal_Code']

        widgets = {
            'city': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'postal_Code': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }


class ItemsForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }


class TimeActivityForm(ModelForm):
    class Meta:
        model = TimeActivity
        fields = ['name_of', 'employee', 'hours', 'hourly_Rate',
                  'transaction_date', 'item']

        widgets = {
            'employee': forms.Select(attrs={
                'class': 'form-select'
            }),
            'name_of': forms.Select(attrs={
                'class': 'form-select'
            }),

            'hours': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'hourly_Rate': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'transaction_date': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'item': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class UpdateTimeActivityForm(ModelForm):
    class Meta:
        model = TimeActivity
        fields = ['name_of', 'employee', 'hours', 'hourly_Rate',
                  'transaction_date', 'sync_token', 'time_activity_id', 'item']

        widgets = {
            'employee': forms.Select(attrs={
                'class': 'form-select'
            }),
            'name_of': forms.Select(attrs={
                'class': 'form-select'
            }),

            'hours': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'hourly_Rate': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'transaction_date': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'sync_token': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'time_activity_id': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'item': forms.Select(attrs={
                'class': 'form-select'
            })
        }
