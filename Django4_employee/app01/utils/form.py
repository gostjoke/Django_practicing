from django.shortcuts import render, redirect
from app01 import models
import datetime
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
# from django.utils.safestring import mark_safe # 分頁
from app01.utils.Pagenation import Pagenation
from app01.utils.BootStrap import BootStrapModelForm

#### login 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class RegisterForm(UserCreationForm):

    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    login_valid = forms.CharField(
        label='驗證碼',
        widget=forms.TextInput,
        required=True
        )


class UserModelForm(forms.ModelForm):

    ### 多規則驗證 如最小字 RE
    name = forms.CharField(min_length=5, max_length=20, label='用戶名')
    password = forms.CharField(min_length=7, max_length=25, label='密碼')#, validators=) 正則


    class Meta:
        model = models.UserInfo
        # name = forms.CharField(min_length=5, max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', "depart"]
        # widgets = {
        #     # "name" : forms.TextInput(attrs={'class': 'form-control'}),
        #     # "password" : forms.PasswordInput(attrs={'class': 'form-control'}),
        #     # "age" : forms.TextInput(attrs={'class': 'form-control'}),
        #     # "account" : forms.TextInput(attrs={'class': 'form-control'}),
        #     # "create_time" : forms.DateInput(attrs={'class': 'form-control'}),
        #     # "gender" : forms.Select(choices=models.UserInfo.gender_choices, attrs={'class': 'form-control'}),
        #     # "depart" : forms.Select(choices=models.Department.objects.all(), attrs={'class': 'form-control'}),
        # }

        widgets = {
            'create_time': forms.SelectDateWidget(attrs={'class': 'date'}),
            # ... (其他字段的小部件定义)
        }
    
    # 循環找到所有插件 並使其符合格式
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        ## 循環model.forms的插件, 給每個字段設插件
        for name, field in self.fields.items():
            if field.widget.attrs: # 有屬性保留原本 沒屬性才設
                field.widget.attrs["class"] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs={'class':'form-control', 
                                    'placeholder': field.label}


    ###

    ######### mobile #########

class PrettyModelForm(BootStrapModelForm):
    # 驗證方式1 
    mobile = forms.CharField(label ='手機號', validators=[RegexValidator(r'^1[3-9]\d{8}$', '手機號格是錯誤')]) #

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        # exclude = ['level']
        fields = ['mobile', 'price', 'level', 'status']
    
        # exclude = ['level']

    
    # 驗證方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']

        # 回查數據 以防重複手機
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise forms.ValidationError('手機號已存在')

        if len(txt_mobile)!= 10:
            raise forms.ValidationError('格式錯誤')
        return txt_mobile
    
#################### PrettyEditModelForm ########################
### 如果我們不想讓他改手機號
### orginial
"""
class PrettyEditModelForm(forms.ModelForm):
    # 驗證方式1 
    # modbile = forms.CharField(label ='手機號', validators=[RegexValidator(r'^1[3-9]\d{9}$', '手機號格是錯誤')]) #
    # 如果想讓手機不能改
    mobile = forms.CharField(label ='手機號', disabled=True)
    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        # exclude = ['level']
        # fields = ['price', 'level', 'status']
        fields = ['mobile', 'price', 'level', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs={'class':'form-control', 'placeholder': field.label}

    # 驗證方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']

        if len(txt_mobile)!= 10:
            raise forms.ValidationError('格式錯誤')
        return txt_mobile
"""    

class PrettyEditModelForm(BootStrapModelForm):
    # 驗證方式1 
    # modbile = forms.CharField(label ='手機號', validators=[RegexValidator(r'^1[3-9]\d{9}$', '手機號格是錯誤')]) #
    # 如果想讓手機不能改
    mobile = forms.CharField(label ='手機號', disabled=True)
    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        # exclude = ['level']
        # fields = ['price', 'level', 'status']
        fields = ['mobile', 'price', 'level', 'status']

    # 驗證方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']

        if len(txt_mobile)!= 10:
            raise forms.ValidationError('格式錯誤')
        return txt_mobile

#####################################################################