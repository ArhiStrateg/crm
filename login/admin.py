from django.contrib import admin
from login.models import User_Login
from projects.admin import Inlines_Comment_For_Project, Inlines_File_For_Project, Inlines_Sub_Project_Prime_Data, \
    Inlines_Data_Prime_Project, Inlines_Prime_Project, Inlines_Sub_Project, Inlines_Incom, Inlines_Incom_Data, Inlines_Outcom,\
    Inlines_Outcom_Data, Inlines_Status_Project, Inlines_File_Incom_Data, Inlines_File_Outcom_Data


class Admin_User_Login (admin.ModelAdmin):
    list_display = [field.name for field in User_Login._meta.fields]
    inlines = [Inlines_Comment_For_Project, Inlines_File_For_Project, Inlines_Sub_Project_Prime_Data,
               Inlines_Data_Prime_Project, Inlines_Prime_Project, Inlines_Sub_Project_Prime_Data, Inlines_Sub_Project, Inlines_Incom,
               Inlines_Incom_Data, Inlines_Outcom, Inlines_Outcom_Data, Inlines_Status_Project, Inlines_File_Incom_Data,
               Inlines_File_Outcom_Data]

    class Meta:
        model = User_Login

admin.site.register(User_Login, Admin_User_Login)