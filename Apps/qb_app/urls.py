from django.urls import path

from Apps.qb_app import views

urlpatterns = [
    path('', views.index),
    path('callback', views.callback, name="callback"),
    path('home', views.home, name="home"),
    path('employee', views.get_employee, name='employee'),
    path('item', views.get_items),
    path('timeActivity', views.get_timeActivity),
    path('fetchData', views.fetchData),
    path('addEmployee', views.add_employee),
    path('additems', views.add_items),
    path('addTimeActivity', views.add_time_activity),
    path('updateTimeActivity', views.update_time_activity),
    path('refreshToken', views.refresh_token)
]
