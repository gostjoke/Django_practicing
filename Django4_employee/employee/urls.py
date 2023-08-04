"""employee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app01.views import depart, pretty, users, sign, task

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login', sign.sign_in, name='Login'),
    path('logout', sign.log_out, name='Logout'),
    path("", depart.index, name='Index'),
    path("image/login_valid", sign.login_valid),
    # path("admin/", admin.site.urls),

    ########## departments ##########
    path("depart/list/", depart.depart_list),
    path("depart/add/", depart.depart_add),
    path("depart/delete/", depart.depart_delete),

    # http://127.0.0.1:8000/depart/10/edit/
    path("depart/<int:nid>/edit/", depart.depart_edit),
    ########## departments ##########


    ########## user_list ##########
    path("user/list/", users.user_list),
    path("user/add/", users.user_add),
    path("user/model/form/add/", users.user_model_form_add),
    path("user/<int:nid>/edit/", users.user_edit),
    path("user/<int:nid>/delete/", users.user_delete),

    ########## pretty_list ##########
    path("pretty/list/", pretty.pretty_list),
    path("pretty/model/form/add/", pretty.pretty_model_form_add),
    path("pretty/<int:nid>/edit/", pretty.pretty_edit),
    path("pretty/<int:nid>/delete/", pretty.pretty_delete),

    ########## tasks list ###########
    path("task/list/", task.task_list),
    path('task/ajax/', task.task_ajax),
]
