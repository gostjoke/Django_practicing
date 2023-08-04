#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file         :pretty.py
@explain      :
@date         :2023/07/28 10:40:35
@author       :Tien-Wei Hsu
@version      :1.0
'''
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app01 import models
import datetime
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
# from django.utils.safestring import mark_safe # 分頁
from app01.utils.Pagenation import Pagenation
from app01.utils.BootStrap import BootStrapModelForm
from app01.utils.form import *

@login_required(login_url="Login")
def pretty_list(request):

    # models.PrettyNum.objects.filter(id=12)
    # models.PrettyNum.objects.filter(id__gt=12) 大於
    # models.PrettyNum.objects.filter(id__gte=12)大於等於
    # models.PrettyNum.objects.filter(id__lt=12) 小於
    # models.PrettyNum.objects.filter(mobile__startswith='') 起始字
    # models.PrettyNum.objects.filter(mobile__endswith='') 結尾字
    # models.PrettyNum.objects.filter(mobile__contains='') 包含
    
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile=str(1000000000+i), price=i, level=1, status=1)
    # models.PrettyNum.objects.all().delete()
    ######### 搜索 #########
    
    data_dict = {}
    search_data = request.GET.get('q', "") # 對應到name ="q"
    
    if search_data:
        data_dict['mobile__contains'] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')

    ##################
    ## 分頁
    ## 組件
    page_object = Pagenation(request=request, queryset=queryset )

    context = {'search_data': search_data,
        
                'queryset': page_object.page_queryset, # 分完頁的數據
               'page_string': page_object.html()} # 生成頁碼


    return render(request, 'pretty_list.html',context)

@login_required(login_url="Login")
def pretty_model_form_add(request):
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_model_form_add.html', {'form': form})  
    
    # need to verify form, 
    form = PrettyModelForm(data = request.POST)
    form.is_valid() # 自動逐一校驗
    
    if form.is_valid():
        print(form.cleaned_data)
        
        form.save() # 保存到資料 不用再create
        return redirect('/pretty/list/')   
    # else:
        # 校驗失敗  並返回原頁面 顯示錯誤 記得novalidate html
    # print(form.errors)
    return render(request, 'pretty_model_form_add.html', {'form': form}) 

@login_required(login_url="Login")
def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')

@login_required(login_url="Login")
def pretty_edit(request, nid):
    ### 編輯手機
    
    row_object = models.PrettyNum.objects.filter(id=nid).first() # get and post 接用
    if request.method == 'GET':
        # 根據ID去數據庫獲取那一行
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})
    
    form = PrettyEditModelForm(data = request.POST, instance=row_object) # 數據更新 data = request.POST
    if form.is_valid():
        # 強迫更改數據
        # form.instance.字段名 = ???
        #默認保存用戶輸入的所有數據 
        form.save() # 
        return redirect('/pretty/list/')

    return render(request, 'pretty_edit.html', {'form': form})

######### mobile #########
