from django.shortcuts import render, HttpResponse, redirect
from intuitlib.client import AuthClient
from quickbooks.objects.customer import Customer
from quickbooks import QuickBooks
from intuitlib.enums import Scopes
from App import qbconnection
from App import models
from App.forms import EmployeeForm, PrimaryAddrForm, ItemsForm, TimeActivityForm, UpdateTimeActivityForm
import requests
import json


qbconn = qbconnection.QuickbooksConnection()


def index(request):
    url = qbconn.auth_client.get_authorization_url([Scopes.ACCOUNTING])
    return redirect(url)


def callback(request):
    qbconn.auth_code = request.GET.get('code', None)
    qbconn.realm_id = request.GET.get('realmId', None)
    request.session['realm_id'] = qbconn.realm_id
    qbconn.auth_client.get_bearer_token(
        qbconn.auth_code, realm_id=qbconn.realm_id)
    qbconn.auth_header = 'Bearer {0}'.format(qbconn.auth_client.access_token)
    return redirect('employee')


def home(request):
    return render(request, 'base.html')


def employee(request):
    response = qbconn.getData(object='employee')
    data = models.Employee.objects.all()
    context = {
        'data': data,
    }

    return render(request, 'employee.html', context=context)


def items(request):
    response = qbconn.getData(object='item')
    data = models.Item.objects.all()
    context = {
        'data': data
    }
    return render(request, 'items.html', context=context)


def timeActivity(request):
    response = qbconn.getData(object='time_activity')
    data = models.TimeActivity.objects.all()
    context = {
        'data': data
    }
    return render(request, 'timeActivities.html', context=context)


def fetchEmployee(request):
    response_emp = qbconn.getData(object='employee')
    response_ta = qbconn.getData(object='time_activity')
    response_item = qbconn.getData(object='item')
    data_emp = json.loads(response_emp.text)
    data_items = json.loads(response_item.text)
    data_ta = json.loads(response_ta.text)
    for employee in data_emp['QueryResponse']['Employee']:
        emp, create = models.Employee.objects.update_or_create(
            given_Name=employee['GivenName'],
            family_Name=employee['FamilyName'],
            qb_EmpId=employee['Id'])
        if('PrimaryAddr' in employee):
            addr, create = models.PrimaryAddr.objects.update_or_create(
                city=employee['PrimaryAddr']['City'],
                postal_Code=employee['PrimaryAddr']['PostalCode'],
                qb_Id=employee['PrimaryAddr']['Id'])
            addr.save()
            emp.primaryAddr = addr
        emp.save()

    for items in data_items['QueryResponse']['Item']:
        items_obj, create = models.Item.objects.update_or_create(
            name=items['Name'], item_id=items['Id'])
        items_obj.save()

    for time_activities in data_ta['QueryResponse']['TimeActivity']:
        time_activitie_obj, create = models.TimeActivity.objects.update_or_create(
            transaction_date=time_activities['TxnDate'],
            hours=time_activities['Hours'],
            qb_employee_id=time_activities['EmployeeRef']['value'],
            employee_name=time_activities['EmployeeRef']['name'],
            hourly_Rate=time_activities['HourlyRate'],
            billable_Status=time_activities['BillableStatus'],
            time_activity_id=time_activities['Id'],
            name_of=time_activities['NameOf']
        )
        emp = models.Employee.objects.filter(
            qb_EmpId=time_activities['EmployeeRef']['value'])
        for emps in emp:

            time_activitie_obj.employee = emps
            time_activitie_obj.save()

    return render(request, 'employee.html')


def addEmployee(request):
    if(request.method == "POST"):

        data = {
            "GivenName": request.POST.get("given_Name"),
            "PrimaryAddr": {
                "City": request.POST.get('city'),
                "PostalCode": request.POST.get('postal_Code'),
            },
            "FamilyName": request.POST.get('family_Name')
        }

        requests.post('{0}/v3/company/{1}/employee'.format(qbconn.base_url,
                                                           qbconn.realm_id), json=data, headers=qbconn.header())
        return redirect('home')
    else:
        empForm = EmployeeForm()
        addrForm = PrimaryAddrForm()
        context = {
            'empForm': empForm,
            'addrForm': addrForm,
            'action': '/addEmployee',
            'form_title': 'Add Employee'
        }
        return render(request, 'form.html', context=context)


def addItems(request):

    if(request.method == "POST"):
        data = {
            "Name": request.POST.get('name'),
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
        requests.post('{0}/v3/company/{1}/item'.format(qbconn.base_url,
                                                       qbconn.realm_id), json=data, headers=qbconn.header())

        redirect('home')
    else:
        itemsForm = ItemsForm()
        context = {
            'form': itemsForm,
            'action': '/additems',
            'form_title': 'Add Item'
        }
        return render(request, 'form.html', context=context)


def addTimeActivity(request):
    if(request.method == "POST"):
        data = {
            "TxnDate": request.POST.get('transaction_date'),
            "Hours": request.POST.get('hours'),
            "HourlyRate": request.POST.get('hourly_Rate'),
            "EmployeeRef": {
                "name": request.POST.get('employee_name'),
                "value": request.POST.get('qb_employee_id')
            },
            "NameOf": 'Employee'
        }
        requests.post('{0}/v3/company/{1}/timeactivity'.format(qbconn.base_url,
                                                               qbconn.realm_id), json=data, headers=qbconn.header())
        return redirect('home')
    else:
        timeActivityForm = TimeActivityForm()
        context = {
            'form': timeActivityForm,
            'action': '/addTimeActivity',
            'form_title': 'Add Time Activity'
        }
        return render(request, 'form.html', context=context)


def updateTimeActivity(request):
    if(request.method == "POST"):
        d = {
            "TxnDate": request.POST.get('transaction_date'),
            "NameOf": "Employee",
            "Hours": request.POST.get('hours'),
            "BillableStatus": "Billable",
            "HourlyRate": request.POST.get('hourly_Rate'),
            "EmployeeRef": {
                "name":  request.POST.get('employee_name'),
                "value": request.POST.get('employee_id')
            },
            "SyncToken": request.POST.get('sync_token'),
            "Id": request.POST.get('time_activity_id'),
        }

        requests.post('{0}/v3/company/{1}/timeactivity'.format(qbconn.base_url,
                                                               qbconn.realm_id), json=d, headers=qbconn.header())
        return redirect('home')
    else:
        timeActivityForm = UpdateTimeActivityForm()
        context = {
            'form': timeActivityForm,
            'action': '/addTimeActivity',
            'form_title': 'Update Time Activity'
        }
        return render(request, 'form.html', context=context)
