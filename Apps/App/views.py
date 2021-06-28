import logging
import requests
from intuitlib.enums import Scopes
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from Apps.App import models
from Apps.App import qbconnection
from Apps.App.filters import TImeActivityFilter
from Apps.App.forms import EmployeeForm, ItemsForm, PrimaryAddrForm, TimeActivityForm, UpdateTimeActivityForm
from Apps.App.tasks import  fetch_qb_data

qbconn = qbconnection.QuickbooksConnection.get_instance()
db_logger = logging.getLogger('db')

def index(request):
    redirect_url = qbconn.auth_client.get_authorization_url([Scopes.ACCOUNTING])
    return redirect(redirect_url)

def callback(request):
    try:
        qbconn.auth_code = request.GET.get('code', None)
        qbconn.realm_id = request.GET.get('realmId', None)
        request.session['realm_id'] = qbconn.realm_id
        qbconn.auth_client.get_bearer_token(
            qbconn.auth_code, realm_id=qbconn.realm_id)
        qbconn.auth_header = 'Bearer {0}'.format(qbconn.auth_client.access_token)
    except Exception as e:
        db_logger.exception(e)
        return redirect('home')
    return redirect('employee')

@login_required(login_url='login')
def home(request):
    return render(request, 'base.html')

def refresh_token(request):
    try:
        qbconn.auth_client.refresh(refresh_token=qbconn.auth_client.refresh_token)
        qbconn.auth_header = 'Bearer {0}'.format(qbconn.auth_client.access_token)
        update_token()
    except Exception as e:
        return HttpResponse('please connect to quickbooks')
    return redirect('employee')

def update_token():
    if(models.Token.objects.all()):
        cel = models.Token.objects.update(bearer = qbconn.auth_header)
    else:
        cel = models.Token.objects.create(bearer = qbconn.auth_header)

@login_required(login_url='login')
def get_employee(request):
    data = models.Employee.objects.all()
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)
    context = {
        'data': data,
    }
    return render(request, 'employee.html', context=context)

@login_required(login_url='login')
def get_items(request):
    items_queryset = models.Item.objects.all()
    paginator = Paginator(items_queryset, 10)
    page_number = request.GET.get('page')
    items_data = paginator.get_page(page_number)
    context = {
        'data': items_data
    }
    return render(request, 'items.html', context=context)

@login_required(login_url='login')
def get_timeActivity(request):
    data = models.TimeActivity.objects.all()
    filter = TImeActivityFilter(request.GET, queryset = data)
    data = filter.qs
    paginator = Paginator(data, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)
    context = {
        'data': data ,
        'filter' : filter
    }
    return render(request, 'timeActivities.html', context=context)

@login_required(login_url='login')
def fetchData(request):
    try:
        r = fetch_qb_data.delay()
    except Exception as e:
        db_logger.exception(e)
    return redirect('home')

@login_required(login_url='login')
def add_employee(request):
    if(request.method == "POST"):
        empForm = EmployeeForm(request.POST)
        addrForm = PrimaryAddrForm(request.POST)
        if(empForm.is_valid()):
            data = {
                "GivenName": request.POST.get("given_Name"),
                "PrimaryAddr": {
                    "City": request.POST.get('city'),
                    "PostalCode": request.POST.get('postal_Code'),
                },
                "FamilyName": request.POST.get('family_Name')
            }
            try:
                requests.post('{0}/v3/company/{1}/employee'.format(qbconn.base_url,
                                                            qbconn.realm_id), json=data, headers=qbconn.header())
            except Exception as e:
                return HttpResponse("please connect to quickbooks")
            return redirect('home')
        else:
            context = {
            'empForm': empForm,
            'addrForm': addrForm,
            'action': '/addEmployee',
            'form_title': 'Add Employee'
            }
            return render(request , 'form.html', context=context)
    
    if(request.method == "GET"):
        empForm = EmployeeForm()
        addrForm = PrimaryAddrForm()
        context = {
            'empForm': empForm,
            'addrForm': addrForm,
            'action': '/addEmployee',
            'form_title': 'Add Employee'
        }
        return render(request, 'form.html', context=context)

@login_required(login_url='login')
def add_items(request):
    if(request.method == "POST"):
        itemsForm = ItemsForm(request.POST)
        if(itemsForm.is_valid()):
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
            try:

                requests.post('{0}/v3/company/{1}/item'.format(qbconn.base_url,
                                                        qbconn.realm_id), json=data, headers=qbconn.header())
            except Exception as e:
                return HttpResponse('please connect to quickbooks')
            return redirect('home')
        else:
            context = {
            'form': itemsForm,
            'action': '/additems',
            'form_title': 'Add Item'
            }
            return render(request , 'form.html' , context=context)

    if(request.method == "GET"):
        itemsForm = ItemsForm()
        context = {
            'form': itemsForm,
            'action': '/additems',
            'form_title': 'Add Item'
        }
        return render(request, 'form.html', context=context)
    
    return redirect('home')

@login_required(login_url='login')
def add_timeActivity(request):
    if(request.method == "POST"):
        time_activity_form = TimeActivityForm(request.POST)
        if time_activity_form.is_valid():

            data = {
                "TxnDate": request.POST.get('transaction_date'),
                "Hours": request.POST.get('hours'),
                "HourlyRate": request.POST.get('hourly_Rate'),
                "EmployeeRef": {
                    "name": models.Employee.objects.get(id = request.POST.get('employee')).given_Name,
                    "value": models.Employee.objects.get(id = request.POST.get('employee')).qb_EmpId
                },
                "ItemRef": {
                "name": models.Item.objects.get(id = request.POST.get('item')).name,
                "value": models.Item.objects.get(id = request.POST.get('item')).item_id,
                },
                "NameOf": 'Employee'
            }
            try:
                requests.post('{0}/v3/company/{1}/timeactivity'.format(qbconn.base_url,
                                                                qbconn.realm_id), json=data, headers=qbconn.header())
            except Exception as e:
                return HttpResponse('please connect to quickbooks')
            return redirect('home')
        else:
            context = {
            'form': time_activity_form,
            'action': '/addTimeActivity',
            'form_title': 'Add Time Activity'
        }
        return render(request, 'form.html', context=context)

    if(request.method == "GET"):
        timeActivityForm = TimeActivityForm()
        context = {
            'form': timeActivityForm,
            'action': '/addTimeActivity',
            'form_title': 'Add Time Activity'
        }
        return render(request, 'form.html', context=context)
    
    return redirect('home')

@login_required(login_url='login')
def update_timeActivity(request):
    if(request.method == "POST"):
        data = {
            "TxnDate": request.POST.get('transaction_date'),
            "NameOf": "Employee",
            "Hours": request.POST.get('hours'),
            "BillableStatus": "Billable",
            "HourlyRate": request.POST.get('hourly_Rate'),
            "EmployeeRef": {
                "name": models.Employee.objects.get(id = request.POST.get('employee')).given_Name,
                "value": models.Employee.objects.get(id = request.POST.get('employee')).qb_EmpId
            },
            "ItemRef": {
            "name": models.Item.objects.get(id = request.POST.get('item')).name,
            "value": models.Item.objects.get(id = request.POST.get('item')).item_id,
            },
            "SyncToken": request.POST.get('sync_token'),
            "Id": request.POST.get('time_activity_id'),
        }
        try:
            requests.post('{0}/v3/company/{1}/timeactivity'.format(qbconn.base_url,
                                                               qbconn.realm_id), json=data, headers=qbconn.header())
        except Exception as e:
                return HttpResponse('please connect to quickbooks')
        return redirect('home')

    if(request.method == "GET"):
        timeActivityForm = UpdateTimeActivityForm()
        context = {
            'form': timeActivityForm,
            'action': '/addTimeActivity',
            'form_title': 'Update Time Activity'
        }
        return render(request, 'form.html', context=context)
    return redirect('home')