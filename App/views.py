from django.shortcuts import render, redirect
from intuitlib.enums import Scopes
from App import qbconnection
from App import models
from App.forms import EmployeeForm, PrimaryAddrForm, ItemsForm, TimeActivityForm, UpdateTimeActivityForm
import requests
import logging
from App.tasks import  fetch
from django.contrib.auth.decorators import login_required
# Let's use Amazon S3




# getting quickbooks connection object instance from singleton QB class.
qbconn = qbconnection.QuickbooksConnection.get_instance()
# db_logger object to log the exceptions in the database
db_logger = logging.getLogger('db')

def index(request):
    # generating the redirect uri for access tokens
    url = qbconn.auth_client.get_authorization_url([Scopes.ACCOUNTING])
    return redirect(url)

# redirect callback uri from Quickbooks
def callback(request):
    qbconn.auth_code = request.GET.get('code', None)
    qbconn.realm_id = request.GET.get('realmId', None)
    request.session['realm_id'] = qbconn.realm_id
    qbconn.auth_client.get_bearer_token(
        qbconn.auth_code, realm_id=qbconn.realm_id)
    qbconn.auth_header = 'Bearer {0}'.format(qbconn.auth_client.access_token)
    return redirect('employee')

@login_required(login_url='login')
def home(request):
    return render(request, 'base.html')

def refresh_token(request):
    qbconn.auth_client.refresh(refresh_token=qbconn.auth_client.refresh_token)
    qbconn.auth_header = 'Bearer {0}'.format(qbconn.auth_client.access_token)
    if(models.Token.objects.all()):
        cel = models.Token.objects.update(bearer = qbconn.auth_header)
    else:
        cel = models.Token.objects.create(bearer = qbconn.auth_header)
    return redirect('home')

def employee(request):
    if(models.Token.objects.all()):
        cel = models.Token.objects.update(bearer = qbconn.auth_header)
    else:
        cel = models.Token.objects.create(bearer = qbconn.auth_header)
    data = models.Employee.objects.all()
    context = {
        'data': data,
    }
    return render(request, 'employee.html', context=context)

def items(request):
    data = models.Item.objects.all()
    context = {
        'data': data
    }
    return render(request, 'items.html', context=context)

def timeActivity(request):
    data = models.TimeActivity.objects.all()
    context = {
        'data': data
    }
    return render(request, 'timeActivities.html', context=context)

#fetch data from Quickbooks online to database at midnight
def fetchData(request):
    try:
        r = fetch.delay()
    except Exception as e:
        #logging to the db if exception occurs at fetching data
        db_logger.exception(e)
    
    return render(request, 'base.html')

#adds new employee to Quickbooks
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
        #redirecting to index.html
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

#add new items to Quickbooks
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
        # redirecting index.html template
        redirect('home')
    else:
        #itemForms from App.forms
        itemsForm = ItemsForm()
        context = {
            'form': itemsForm,
            'action': '/additems',
            'form_title': 'Add Item'
        }
        return render(request, 'form.html', context=context)

#Add new timeActivity to Quickbooks using portals
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
        # TimeActivityForm from App.forms
        timeActivityForm = TimeActivityForm()
        context = {
            'form': timeActivityForm,
            'action': '/addTimeActivity',
            'form_title': 'Add Time Activity'
        }
        return render(request, 'form.html', context=context)

#update timeActivity post request to Quickbooks
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
        # redirecting to the index.html
        return redirect('home')
    else:
        timeActivityForm = UpdateTimeActivityForm()
        context = {
            'form': timeActivityForm,
            'action': '/addTimeActivity',
            'form_title': 'Update Time Activity'
        }
        return render(request, 'form.html', context=context)
