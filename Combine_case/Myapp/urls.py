from . import views
from django.urls import path #,include

urlpatterns = [
    path('', views.index, name='Index'),
    path('register', views.sign_up, name='Register'),
    path('login', views.sign_in, name='Login'),
    path('logout', views.log_out, name='Logout'),
    path('table', views.table_create, name="Table"),
    path('input', views.input, name="Input"),
    path('Update/<str:pk>', views.update, name='Update'),
    path('delete/<str:pk>', views.delete, name='Delete')
]
