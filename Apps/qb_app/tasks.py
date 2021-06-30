import django
import json
import requests

from celery import shared_task

from quickbookIntegration.celery import app
from Apps.qb_app.constants import BASE_URL , EMPLOYEE , ITEM , TIME_ACTIVITY
django.setup()
from Apps.qb_app import models, utils


@shared_task
def fetch_qb_data_and_store_in_db():
    store_employee_data_in_db()
    store_item_data_db()
    store_time_activity_data_in_db()
    return ("Data Fetched sucessfully")


def store_employee_data_in_db():
    response_emp = get_response_data('employee')
    data_emp = json.loads(response_emp.text)
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


def store_item_data_db():
    response_item = get_response_data('item')
    data_items = json.loads(response_item.text)
    for items in data_items['QueryResponse']['Item']:
        items_obj, create = models.Item.objects.update_or_create(
            name=items['Name'], item_id=items['Id'])
        items_obj.save()


def store_time_activity_data_in_db():
    response_ta = get_response_data('time_activity')
    data_ta = json.loads(response_ta.text)
    for time_activities in data_ta['QueryResponse']['TimeActivity']:
        time_activitie_obj, create = models.TimeActivity.objects.update_or_create(
            transaction_date=time_activities['TxnDate'],
            hours=time_activities['Hours'],
            hourly_Rate=time_activities['HourlyRate'],
            billable_Status=time_activities['BillableStatus'],
            time_activity_id=time_activities['Id'],
            name_of=time_activities['NameOf'],
        )
        emp = models.Employee.objects.filter(
            qb_EmpId=time_activities['EmployeeRef']['value'])
        for emps in emp:
            time_activitie_obj.employee = emps
            time_activitie_obj.save()

        item = models.Item.objects.filter(
            item_id=time_activities['ItemRef']['value'])

        for items in item:
            time_activitie_obj.item = items
            time_activitie_obj.save()


def get_response_data(object):
    if object == 'employee':
        query = EMPLOYEE
    elif object == 'item':
        query = ITEM
    elif object == 'time_activity':
        query = TIME_ACTIVITY
    query_url = '{0}/v3/company/4620816365171746060/query?query={1}'.format(
        BASE_URL, query)
    return requests.get(query_url, headers=utils.get_header())
