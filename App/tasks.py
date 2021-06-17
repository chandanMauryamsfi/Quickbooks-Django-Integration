from quickbookIntegration.celery import app
from celery import shared_task
import json
import requests
import django
django.setup()
from App import models



@shared_task
def fetch():
    response_emp = getdata('employee')
    response_ta = getdata('time_activity')
    response_item = getdata('item')
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
    return ("Data Fetched")


def getdata(object):
    if object == 'employee':
        query = 'select * from Employee'
    elif object == 'item':
        query = 'select * from Item'
    elif object == 'time_activity':
        query = 'select * from TimeActivity'
    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    header = {
            'Authorization': models.Token.objects.all()[0].bearer,
            'Accept': 'application/json'
        }
    url = '{0}/v3/company/4620816365171746060/query?query={1}'.format(
            base_url,query)
    return requests.get(url, headers=header)