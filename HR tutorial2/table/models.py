from django.db import models
from datetime import timedelta

# Create your models here.
"""
CharField 字串欄位
IntegerField 整數欄位
FloatField 浮點數欄位
DateField 日期欄位
ImageField 圖片欄位
"""
# ID number employee

class department(models.Model):
    department_name = models.CharField(max_length=12, primary_key=True)
    department_information = models.CharField(max_length=255)

    def __str__(self):
        return self.department_name
    

class employee(models.Model):
    emp_id = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=255)
    department_name = models.ForeignKey(department,on_delete=models.CASCADE)

    def __str__(self):
        return self.emp_id

class vaction(models.Model):
    vaction_start = models.DateField()
    vaction_end = models.DateField()
    vaction_length = models.DurationField(db_column='date')

    emp_id =models.ForeignKey(employee,on_delete=models.CASCADE)

