
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
########## user ##########
@login_required(login_url="Login")
def user_list(request):
    # queryset = models.UserInfo.objects.all()
    data_dict = {}
    search_data = request.GET.get('q', "") # 對應到name ="q"
    
    if search_data:
        data_dict['id__contains'] = search_data

    queryset = models.UserInfo.objects.filter(**data_dict).order_by('id') # -id 反向
    """
    for obj in queryset:
        print(obj.id, obj.name, obj.password, obj.age, obj.account, 
        obj.create_time.strftime('%Y-%m-%d'),obj.depart.title ,
        obj.get_gender_display())
        
        ### obj.get_gender_display() 特殊用法

        ### 其中一種拿法
        # models.Department.objects.filter(id=obj.depart).first().title
        # 可直接用 obj.depart.title
    """

    page_object = Pagenation(request, queryset, page_size=5)
    
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }

    return render(request, 'user_list.html', context)

@login_required(login_url="Login")
def user_add(request):
    if request.method == 'GET':
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all(),
        }

        return render(request, 'user_add.html', context)
    elif request.method == 'POST':
        # ['user', 'password', 'age', 'account', 'create_time', 'gender', "depart"]
        
        ## 數據校驗無法 所以必須重寫
        user = request.POST.get('user')
        password =request.POST.get('password')
        age = request.POST.get('age')
        account = request.POST.get('account')
        create_time = request.POST.get('create_time')
        gender_id = request.POST.get('gender')
        depart_id = request.POST.get('depart')
        
        models.UserInfo.objects.create(name=user, password=password, 
                                       age=age, account=account, create_time=create_time, 
                                       gender=gender_id, depart_id=depart_id)

        return redirect('/user/list/')
    


@login_required(login_url="Login")
def user_model_form_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {'form': form})  
    
    # need to verify form, 
    form = UserModelForm(data = request.POST)
    form.is_valid() # 自動逐一校驗
    
    if form.is_valid():
        print(form.cleaned_data)
        # {'name': 'Uincode', 'password': '456', 'age': 32, 'account': Decimal('67'), 'create_time': datetime.datetime(2012, 11, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'gender': 1, 'depart': <Department: PM/BD>}
        form.save() # 保存到資料 不用再create
        return redirect('/user/list/')   
    # else:
        # 校驗失敗  並返回原頁面 顯示錯誤 記得novalidate html
    print(form.errors)
    return render(request, 'user_model_form_add.html', {'form': form}) 
    
@login_required(login_url="Login")
def user_edit(request, nid):
    ### 編輯用戶
    row_object = models.UserInfo.objects.filter(id=nid).first() # get and post 接用
    if request.method == 'GET':
        # 根據ID去數據庫獲取那一行
        # row_object = models.UserInfo.objects.filter(id=nid).first() # first 使
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form, 'nid': nid})
    
    form = UserModelForm(data = request.POST, instance=row_object) # 數據更新 data = request.POST
    if form.is_valid():
        # 強迫更改數據
        # form.instance.字段名 = ???
        #默認保存用戶輸入的所有數據 
        form.save() # 
        return redirect('/user/list/')


    return render(request, 'user_edit.html', {'form': form})

@login_required(login_url="Login")
def user_delete(request, nid):

    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
########## user ##########