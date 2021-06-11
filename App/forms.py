from App.models import Employee, Item, PrimaryAddr, TimeActivity
from django.forms import ModelForm


class EmployeeForm(ModelForm):

    class Meta:
        model = Employee
        fields = ['given_Name', 'family_Name']


class PrimaryAddrForm(ModelForm):
    class Meta:
        model = PrimaryAddr
        fields = ['city', 'postal_Code']


class ItemsForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name']


class TimeActivityForm(ModelForm):
    class Meta:
        model = TimeActivity
        fields = ['name_of', 'employee_name', 'hours', 'hourly_Rate',
                  'qb_employee_id', 'transaction_date']


class UpdateTimeActivityForm(ModelForm):
    class Meta:
        model = TimeActivity
        fields = ['name_of', 'employee_name', 'hours', 'hourly_Rate',
                  'qb_employee_id', 'transaction_date', 'sync_token', 'time_activity_id']
