from django import forms

########## 父類 表##########

class BootStrapModelForm(forms.ModelForm):

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
                

