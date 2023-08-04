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
# Create your views here.

def index(request):
    return render(request, 'index.html')

########## departments ##########
def depart_list(request):
    
    # 獲取所有部門列表
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})

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

########## user ##########
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

def user_delete(request, nid):

    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
########## user ##########


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
    print(form.errors)
    return render(request, 'pretty_model_form_add.html', {'form': form}) 
    

def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')




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




