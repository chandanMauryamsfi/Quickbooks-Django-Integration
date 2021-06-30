from django.contrib import admin
from django.urls import path
from Apps.todoApp import views

urlpatterns = [
    path("todo" , views.index , name='todoPage'),
    path('login/', views.login, name="login"),
    path('signup/', views.sign_up, name="signup"),
    path('addTodo/', views.add_todo, name="add-todo"),
    path('logout/', views.logout, name="logout"),
    path('deleteTodo/<int:id>', views.delete_todo, name="deleteTodo"),
    path('changeStatus/<int:id>/<str:status>',
         views.change_status, name="changeStatus"),
]