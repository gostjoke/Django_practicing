from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app01 import models
import datetime
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
# from django.utils.safestring import mark_safe # 分頁
from app01.utils.Pagenation import Pagenation
from app01.utils.BootStrap import BootStrapModelForm
from app01.utils.form import *

# Create your views here.
@login_required(login_url="Login")
def index(request):
    return render(request, 'index.html')

########## departments ##########
@login_required(login_url="Login")
def depart_list(request):
    
    # 獲取所有部門列表
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})

@login_required(login_url="Login")
def depart_add(request):
    """新增部門"""
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    elif request.method == 'POST':
        # title 為空有組件
        title = request.POST.get('title')

        # 保存到數據庫
        models.Department.objects.create(title=title)

        # 回到部門列表
        return redirect('/depart/list/')

def depart_delete(request):
    """delete department"""
    nid = request.GET.get('nid') # 不是post
    models.Department.objects.filter(id=nid).delete()
    # 回到部門列表
    return redirect('/depart/list/')

def depart_edit(request, nid):
    """edit department"""
    if request.method == 'GET':
        # 根據nid 獲取他的數據 [obj.]
        row_object = models.Department.objects.filter(id=nid).first() # first 使其不是queryset
        # row_object.id
        # nid = request.GET.get('nid') # 不是post
        return render(request, 'depart_edit.html', {'row_object': row_object})
    
    title = request.POST.get('title')
    # models.Department.objects.filter(id=nid).update(title=title, others= .....)
    models.Department.objects.filter(id=nid).update(title=title)

    return redirect('/depart/list/')

########## departments ##########