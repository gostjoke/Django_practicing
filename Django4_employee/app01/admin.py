from django.contrib import admin
from app01.models import Department, UserInfo, PrettyNum
# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id','name','password','age', 'account', 'create_time', 'depart', 'gender')
    # exclude =()

class PrettyNumAdmin(admin.ModelAdmin):
    list_display = ('id','mobile', 'price', 'level', 'status') 


admin.site.register(Department, DepartmentAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(PrettyNum, PrettyNumAdmin)