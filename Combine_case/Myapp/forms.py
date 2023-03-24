from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import vaction


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
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )



class vactionModelForm(forms.ModelForm):

    class Meta:

        model = vaction
        fields = '__all__'
        widgets = {
            'emp_id': forms.Select(attrs={'class': 'form-control'}),
            'vaction_start': forms.SelectDateWidget(attrs={'class': 'date'}),
            'vaction_end': forms.SelectDateWidget(attrs={'class': 'date'}),
            'vaction_length': forms.TextInput(attrs={'class': 'form-control'})
        }  ## 另外，Django ModelForm也提供了widgets屬性，用來客製化表單的顯示外觀，這邊套用Bootstrap的表單CSS類別為例：

        labels = {
            'emp_id': 'Employee ID',
            'vaction_start': 'Vaction Start  ',
            'vaction_end': 'Vaction End   ',
            'vaction_length': 'Vaction Length'
        }


