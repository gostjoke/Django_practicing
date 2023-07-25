from django.db import models
"""
python manage.py makemigrations
python manage.py migrate
"""

# Create your models here.
class Department(models.Model):
    "Department"
    id = models.BigAutoField(verbose_name="ID", primary_key=True)
    title = models.CharField(verbose_name="部門", max_length=32)
    
    def __str__(self):
        return self.title
    ""
class UserInfo(models.Model):
    """ Employee Info """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密碼", max_length=64)
    age = models.IntegerField(verbose_name="年齡")
    account = models.DecimalField(verbose_name="餘額", max_digits=10 ,decimal_places=2)
    # create_time = models.DateTimeField(verbose_name="入職時間")#, auto_now_add=True)
    create_time = models.DateField(verbose_name="入職時間")
    # to 對應 table, to_filed 對應 col
    # depart 會自動生成depart_id
    # depart = models.ForeignKey(to=Department, to_field="id", on_delete=models.CASCADE, verbose_name = "department_id", null=True, blank=True)
    depart = models.ForeignKey(to=Department, to_field="id", on_delete=models.SET_NULL, verbose_name = "部門", null=True, blank=True)

    gender_choices = (
        (1, "male"),
        (2, "female"),
    )
    gender = models.SmallIntegerField(verbose_name="gender", choices=gender_choices)


class PrettyNum(models.Model):
    """ phone number """
    mobile = models.CharField(verbose_name="手機號", max_length=10)
    price = models.IntegerField(verbose_name="價格", default=0, null=True, blank=True)

    level_choices = (
        (1, "1級"),
        (2, "2級"),
        (3, "3級"),
        (4, "4級"),
        )
    
    level = models.SmallIntegerField(verbose_name="級別", choices=level_choices)

    status_choices = (
        (1, "正常"),
        (2, "停用"),
        )
    
    status = models.SmallIntegerField(verbose_name="狀態", choices=status_choices, default=2)



