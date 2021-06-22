from os import path
from django.db import models
import uuid

# Create your models here.
class PrimaryAddr(models.Model):
    city = models.CharField(max_length=50)
    postal_Code = models.CharField(max_length=10)
    qb_Id = models.IntegerField(null=True)

    def __str__(self):
        return self.city


class Employee(models.Model):
    given_Name = models.CharField(max_length=50)
    family_Name = models.CharField(max_length=50)
    qb_EmpId = models.IntegerField()
    primaryAddr = models.ForeignKey(
        PrimaryAddr, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.given_Name +" "+ self.family_Name


class Item(models.Model):
    name = models.CharField(max_length=50)
    item_id = models.IntegerField()

    def __str__(self):
        return self.name


class TimeActivity(models.Model):
    name_of_choice = [
        ('Employee', 'Employee'),
        ('Vendor', 'Vendor')
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    transaction_date = models.DateField()
    hours = models.IntegerField()
    billable_Status = models.CharField(max_length=50)
    hourly_Rate = models.IntegerField()
    time_activity_id = models.IntegerField()
    sync_token = models.IntegerField(default=0)
    name_of = models.CharField(
        max_length=10, choices=name_of_choice, default='Employee')
    item = models.ForeignKey(Item, on_delete=models.CASCADE ,null=True)

    def __str__(self):
        return str(self.employee)

class Token(models.Model):
    bearer = models.CharField(max_length=10000)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)



class Photo(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True) 
    title = models.CharField(max_length=100)
    photo = models.ImageField()