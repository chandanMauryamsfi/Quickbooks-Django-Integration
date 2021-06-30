import logging
import requests

from intuitlib.enums import Scopes

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from Apps.qb_app import models
from Apps.qb_app import qbconnection
from Apps.qb_app.constants import BASE_URL
from Apps.qb_app.filters import TImeActivityFilter
from Apps.qb_app.forms import EmployeeForm, ItemsForm, PrimaryAddrForm, TimeActivityForm, UpdateTimeActivityForm
from Apps.qb_app.tasks import fetch_qb_data_and_store_in_db
from Apps.qb_app.utils import set_pagination

qbconn = qbconnection.QuickbooksConnection.get_instance()
db_logger = logging.getLogger('db')


def index(request):
    redirect_url = qbconn.auth_client.get_authorization_url(
        [Scopes.ACCOUNTING])
    return redirect(redirect_url)


def callback(request):
    try:
        qbconn.auth_code = request.GET.get('code', None)
        qbconn.realm_id = request.GET.get('realmId', None)
        qbconn.auth_client.get_bearer_token(
            qbconn.auth_code, realm_id=qbconn.realm_id)
        qbconn.auth_header = 'Bearer {0}'.format(
            qbconn.auth_client.access_token)
    except Exception as e:
        db_logger.exception(e)
        return redirect('home')
    return redirect('employee')


@login_required(login_url='login')
def home(request):
    return render(request, 'base.html')


def refresh_token(request):
    try:
        qbconn.auth_client.refresh(
            refresh_token=qbconn.auth_client.refresh_token)
        qbconn.auth_header = 'Bearer {0}'.format(
            qbconn.auth_client.access_token)
        update_or_create_token()
    except Exception as e:
        return HttpResponse('please connect to quickbooks')
    return redirect('employee')


@login_required(login_url='login')
def get_employee(request):
    employee_data = models.Employee.objects.all()
    paginated_employee_data = set_pagination(
        request=request, model_data=employee_data)
    context = {
        'data': paginated_employee_data,
    }
    return render(request, 'employee.html', context=context)


def update_or_create_token():
    if(models.Token.objects.all()):
        models.Token.objects.update(bearer=qbconn.auth_header)
    else:
        models.Token.objects.create(bearer=qbconn.auth_header)


@login_required(login_url='login')
def get_items(request):
    items_queryset = models.Item.objects.all()
    items_data = set_pagination(request=request, model_data=items_queryset)
    context = {
        'data': items_data
    }
    return render(request, 'items.html', context=context)


@login_required(login_url='login')
def get_timeActivity(request):
    time_activity_queryset = models.TimeActivity.objects.all()
    filter = TImeActivityFilter(request.GET, queryset=time_activity_queryset)
    time_activity_filter = filter.qs
    time_activity_paginated_filter_data = set_pagination(
        request=request, model_data=time_activity_filter)
    context = {
        'data': time_activity_paginated_filter_data,
        'filter': filter
    }
    return render(request, 'timeActivities.html', context=context)


@login_required(login_url='login')
def fetchData(request):
    try:
        fetch_qb_data_and_store_in_db.delay()
    except Exception as e:
        db_logger.exception(e)
    return redirect('home')


@login_required(login_url='login')
def add_employee(request):
    if(request.method == "POST"):
        empForm = EmployeeForm(request.POST)
        addrForm = PrimaryAddrForm(request.POST)
        if(empForm.is_valid()):
            data = get_employee_dic(model_data=request.POST.get)
            try:
                requests.post('{0}/v3/company/{1}/employee'.format(qbconn.base_url,
                                                                   qbconn.realm_id), json=data, headers=qbconn.header())
            except Exception as e:
                return HttpResponse("please connect to quickbooks")
            return redirect('home')
        else:
            context = get_employee_context_data(
                empForm=empForm, addrForm=addrForm)
            return render(request, 'form.html', context=context)

    if(request.method == "GET"):
        empForm = EmployeeForm()
        addrForm = PrimaryAddrForm()
        context = get_employee_context_data(empForm=empForm, addrForm=addrForm)
        return render(request, 'form.html', context=context)


def get_employee_dic(model_data):
    return {
        "GivenName": model_data("given_Name"),
        "PrimaryAddr": {
            "City": model_data('city'),
            "PostalCode": model_data('postal_Code'),
        },
        "FamilyName": model_data('family_Name')
    }


def get_employee_context_data(empForm, addrForm):
    context = {
        'empForm': empForm,
        'addrForm': addrForm,
        'action': '/addEmployee',
        'form_title': 'Add Employee'
    }
    return context


@login_required(login_url='login')
def add_items(request):
    if(request.method == "POST"):
        itemsForm = ItemsForm(request.POST)
        if(itemsForm.is_valid()):
            data = get_items_dic(request.POST.get)
            try:
                requests.post('{0}/v3/company/{1}/item'.format(BASE_URL,
                                                               qbconn.realm_id), json=data, headers=qbconn.header())
            except Exception as e:
                return HttpResponse('please connect to quickbooks')
            return redirect('home')
        else:
            context = get_items_context_data(itemsForm=itemsForm)
            return render(request, 'form.html', context=context)

    if(request.method == "GET"):
        itemsForm = ItemsForm()
        context = get_items_context_data(itemsForm=itemsForm)
        return render(request, 'form.html', context=context)

    return redirect('home')


def get_items_dic(model_data):
    data = {
        "Name": model_data('name'),
        "QtyOnHand": 10,
        "IncomeAccountRef": {
            "name": "Sales of Product Income",
                    "value": "79"
        },
        "Type": "Inventory",
                "ExpenseAccountRef": {
                    "name": "Cost of Goods Sold",
                    "value": "80"
        }
    }
    return data


def get_items_context_data(itemsForm):
    context = {
        'form': itemsForm,
        'action': '/additems',
        'form_title': 'Add Item'
    }
    return context


@login_required(login_url='login')
def add_time_activity(request):
    if(request.method == "POST"):
        time_activity_form = TimeActivityForm(request.POST)
        if time_activity_form.is_valid():
            time_activity_data = get_time_activity_dic(model_data=request.POST.get)
            try:
                requests.post('{0}/v3/company/{1}/timeactivity'.format(BASE_URL,
                                                                       qbconn.realm_id), json=time_activity_data, headers=qbconn.header())
            except Exception as e:
                return HttpResponse('please connect to quickbooks')
            return redirect('home')
        else:
            context = get_time_activity_context_data(
                time_activity_form=time_activity_form)
        return render(request, 'form.html', context=context)

    if(request.method == "GET"):
        time_activity_form = TimeActivityForm()
        context = get_time_activity_context_data(
            time_activity_form=time_activity_form)
        return render(request, 'form.html', context=context)
    return redirect('home')


def get_time_activity_context_data(time_activity_form):
    context = {
        'form': time_activity_form,
        'action': '/addTimeActivity',
        'form_title': 'Add Time Activity'
    }
    return context


@login_required(login_url='login')
def update_time_activity(request):
    if(request.method == "POST"):
        time_activity_update_data = get_time_activity_updated_dic(model_data=request.POST.get)
        try:
            requests.post('{0}/v3/company/{1}/timeactivity'.format(BASE_URL,
                                                                   qbconn.realm_id), json=time_activity_update_data, headers=qbconn.header())
        except Exception as e:
            return HttpResponse('please connect to quickbooks')
        return redirect('home')

    if(request.method == "GET"):
        time_activity_form = UpdateTimeActivityForm()
        context = get_time_activity_context_data(
            time_activity_form=time_activity_form)
        return render(request, 'form.html', context=context)
    return redirect('home')


def get_time_activity_dic(model_data):
    data = {
        "TxnDate": model_data('transaction_date'),
        "Hours": model_data('hours'),
        "HourlyRate": model_data('hourly_Rate'),
        "EmployeeRef": {
            "name": models.Employee.objects.get(id=model_data('employee')).given_Name,
            "value": models.Employee.objects.get(id=model_data('employee')).qb_EmpId
        },
        "ItemRef": {
            "name": models.Item.objects.get(id=model_data('item')).name,
            "value": models.Item.objects.get(id=model_data('item')).item_id,
        },
        "NameOf": 'Employee'
    }
    return data


def get_time_activity_updated_dic(model_data):
    data = {
        "TxnDate": model_data('transaction_date'),
        "NameOf": "Employee",
        "Hours": model_data('hours'),
        "BillableStatus": "Billable",
        "HourlyRate": model_data('hourly_Rate'),
        "EmployeeRef": {
            "name": models.Employee.objects.get(id=model_data('employee')).given_Name,
            "value": models.Employee.objects.get(id=model_data('employee')).qb_EmpId
        },
        "ItemRef": {
            "name": models.Item.objects.get(id=model_data('item')).name,
            "value": models.Item.objects.get(id=model_data('item')).item_id,
        },
        "SyncToken": model_data('sync_token'),
        "Id": model_data('time_activity_id'),
    }
    return data
