from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from app01.utils.form import RegisterForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

# from .form import vactionModelForm
from django import forms

### image/login_valid
from app01.utils.login_valid import check_code
### image/login_valid


def sign_in(request):

    if request.path_info in ['/login/', '/image/login_valid/', '/login?next=/']:
        return render
    
    form = LoginForm(data=request.POST)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        ## 驗證碼
        if form.is_valid():
            user_input_code = form.cleaned_data.pop('login_valid')
            image_code = request.session.get('login_valid', "")
            if image_code.upper() != user_input_code.upper():
                form.add_error("login_valid", "驗證碼錯誤")
                context = {
                'form': form
                }

                return render(request, 'login.html', context)

        if user is not None:
            login(request, user)
            return redirect('/')  #重新導向到首頁

    context = {
        'form': form
    }
    return render(request, 'login.html', context)


from io import BytesIO

def log_out(request):

    logout(request)

    return redirect('/login') #重新導向到登入畫面

def login_valid(request):
    """picture validator"""
    img, code_string = check_code()

     ## save str to session
    request.session['login_valid'] = code_string
    ## 60 sec 超時 # 保存七天
    request.session.set_expiry(60 * 60 * 24 * 7)
    
    print(code_string)
    stream = BytesIO()
    img.save(stream, 'png')




    return HttpResponse(stream.getvalue())