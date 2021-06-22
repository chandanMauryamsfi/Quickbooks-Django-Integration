from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from todoApp.forms import TodoForm
from todoApp.models import Todo
from django.contrib.auth.decorators import login_required
# Create your views here.


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


def signUp(request):
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
def addTodo(request):

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


def deleteTodo(request, id):
    Todo.objects.get(pk=id).delete()
    return redirect('todoPage')


def changeStatus(request, id, status):
    todo = Todo.objects.get(pk=id)
    todo.status = status
    print(todo.status)
    todo.save()
    return redirect('todoPage')
