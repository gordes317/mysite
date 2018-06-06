from django import forms
from django.contrib.auth.models import User
from .models import UserProfle,UserInfo

# forms.py是一个表单类文件
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    """
    重新定义pasword和password2两个数据模型字段,覆盖内部类Meta中声明数据模型的字段
    """
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)

    class Meta:
        """
        声明本表单类所应用的数据模型,即将来表单的内容会写入到哪个数据库表中的哪些记录里面.
        """
        model = User
        fields = ("username","email")

    def clean_password2(self):
        """
        检验用户所输入的两个密码是否一致
        :return:
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("password do not match")
        return cd['password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfle
        fields = ("phone", "birth")

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school","company","profession","address","aboutme","photo")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)