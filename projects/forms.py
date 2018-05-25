from django import forms
from login.models import User_Login
from django.contrib.admin import widgets

class Form_Create_New_Project(forms.Form):

    name = forms.CharField(max_length=64)
    description_project = forms.CharField(max_length=256, widget=forms.Textarea)
    # who_create_project = forms.ModelChoiceField(queryset=User_Login.objects.all())
    who_boss_project = forms.ModelChoiceField(queryset=User_Login.objects.all())
    date_start_project = forms.DateField(widget=forms.SelectDateWidget)
    date_deadline_project = forms.DateField(widget=forms.SelectDateWidget)


class Form_Create_New_SUBProject(forms.Form):

    name = forms.CharField(max_length=64)
    description_project = forms.CharField(max_length=256, widget=forms.Textarea)
    who_boss_project = forms.ModelChoiceField(queryset=User_Login.objects.all())
    date_start_project = forms.DateField(widget=forms.SelectDateWidget)
    date_deadline_project = forms.DateField(widget=forms.SelectDateWidget)

