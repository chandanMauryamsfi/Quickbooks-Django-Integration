from django.contrib import admin
from django.urls import path
from todoApp import views

urlpatterns = [
    path("todo" , views.index, name="home"),
    path('login/', views.login, name="login"),
    path('signup/', views.signUp, name="signup"),
    path('addTodo/', views.addTodo, name="add-todo"),
    path('logout/', views.logout, name="logout"),
    path('deleteTodo/<int:id>', views.deleteTodo, name="deleteTodo"),
    path('changeStatus/<int:id>/<str:status>',
         views.changeStatus, name="changeStatus"),
]