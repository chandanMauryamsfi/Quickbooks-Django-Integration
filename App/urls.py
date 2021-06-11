from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('', views.index),
    path('callback', views.callback, name="callback"),
    path('home', views.home, name="home"),
    path('employee', views.employee, name='employee'),
    path('item', views.items),
    path('timeActivity', views.timeActivity),
    path('fetchEmployee', views.fetchEmployee),
    path('addEmployee', views.addEmployee),
    path('additems', views.addItems),
    path('addTimeActivity', views.addTimeActivity),
    path('updateTimeActivity', views.updateTimeActivity)
]
