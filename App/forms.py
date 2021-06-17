from App.models import Employee, Item, PrimaryAddr, TimeActivity
from django.forms import ModelForm
from django import forms

class EmployeeForm(ModelForm):

    class Meta:
        model = Employee
        fields = ['given_Name', 'family_Name']

        widgets = {
            'given_Name' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'family_Name' : forms.TextInput(attrs={
                'class' : 'form-control'
            })
        }


class PrimaryAddrForm(ModelForm):
    class Meta:
        model = PrimaryAddr
        fields = ['city', 'postal_Code']
    
        widgets = {
            'city' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'postal_Code' : forms.TextInput(attrs={
                'class' : 'form-control'
            })
        }

class ItemsForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name']

        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'form-control'
            })
        }


class TimeActivityForm(ModelForm):
    class Meta:
        model = TimeActivity
        fields = ['name_of', 'employee_name', 'hours', 'hourly_Rate',
                  'qb_employee_id', 'transaction_date']
        
        widgets = {
            'name_of' : forms.Select(attrs={
                'class' : 'form-select'
            }),
            'employee_name' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'hours' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'hourly_Rate' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'qb_employee_id' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'transaction_date' : forms.TextInput(attrs={
                'class' : 'form-control'
            })
        }


class UpdateTimeActivityForm(ModelForm):
    class Meta:
        model = TimeActivity
        fields = ['name_of', 'employee_name', 'hours', 'hourly_Rate',
                  'qb_employee_id', 'transaction_date', 'sync_token', 'time_activity_id']

        widgets = {
            'name_of' : forms.Select(attrs={
                'class' : 'form-select'
            }),
            'employee_name' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'hours' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'hourly_Rate' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'qb_employee_id' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'transaction_date' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'sync_token' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'time_activity_id' : forms.TextInput(attrs={
                'class' : 'form-control'
            })
            
        }
