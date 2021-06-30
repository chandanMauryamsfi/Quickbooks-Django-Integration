from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from django.contrib.auth.decorators import login_required

from Apps.todo.forms import TodoForm
from Apps.todo.models import Todo


@login_required(login_url='login')
def index(request):
    if request.user.is_authenticated:
        form = TodoForm()
        user = request.user
        todos = Todo.objects.filter(user=user)
        context = {
            'form': form,
            'todos': todos
        }
        return render(request, "index.html", context=context)


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request, "login.html", context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            context = {
                "form": form
            }
            return render(request, "login.html", context=context)


def sign_up(request):
    if request.method == "GET":
        form = UserCreationForm()
        context = {
            'form': form
        }
        return render(request, "signup.html", context=context)
    else:
        form = UserCreationForm(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('login')
        else:
            return render(request, "signup.html", context=context)


@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return redirect('todoPage')
        else:
            context = {
                'form': form,
            }
            return render(request, "index.html", context=context)


@login_required(login_url='login')
def logout(request):
    logoutUser(request)
    return redirect('login')


def delete_todo(request, id):
    Todo.objects.get(pk=id).delete()
    return redirect('todoPage')


def change_status(request, id, status):
    todo = Todo.objects.get(pk=id)
    todo.status = status
    print(todo.status)
    todo.save()
    return redirect('todoPage')
