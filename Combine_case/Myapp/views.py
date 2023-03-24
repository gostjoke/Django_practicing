from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, LoginForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .forms import vactionModelForm

#首頁
@login_required(login_url="Login")
def index(request):
    return render(request, 'Myapp/index.html')

#註冊

def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('/login')  #重新導向到登入畫面
    context = {
        'form': form
    }
    return render(request, 'Myapp/register.html', context)

#登入

def sign_in(request):

    form = LoginForm()


    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  #重新導向到首頁

    context = {
        'form': form
    }
    return render(request, 'Myapp/login.html', context)

# 登出
def log_out(request):

    logout(request)

    return redirect('/login') #重新導向到登入畫面


#### table
from .models import vaction

# Create your views here.
@login_required(login_url="Login")
def table_create(request):

    table = vaction.objects.all()

    return render(request, 'Myapp/table.html',{"tables": table})



##############
@login_required(login_url="Login")
def input(request):

    table = vaction.objects.all()

    form = vactionModelForm

    if request.method == 'POST':
        form = vactionModelForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/input") #?

    context = {
        'tables':table,
        'form':form
    }


    return render(request, 'Myapp/input.html', context)

@login_required(login_url="Login")
def update(request, pk):


    table = vaction.objects.get(id=pk)

    form = vactionModelForm(instance=table)

    if request.method == 'POST':

        form = vactionModelForm(request.POST, instance=table)
        
        if form.is_valid():

            form.save()

        return redirect('/input')
    
    context = {
        'form': form
    }

    return render(request, 'Myapp/update.html', context)

@login_required(login_url="Login")
def delete(request, pk):

    table = vaction.objects.get(id=pk)

    if request.method == "POST":
        table.delete()
        return redirect('/table')


    context = {
        'tables': table
    }

    return render(request, 'Myapp/delete.html', context)