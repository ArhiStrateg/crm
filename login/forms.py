from django import forms
from login.models import User_Login

class Login_Form(forms.ModelForm):

    class Meta:
        model = User_Login;
        fields = ['name_login', 'password_login']
