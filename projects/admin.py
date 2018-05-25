from django.contrib import admin
from projects.models import Prime_Project, Data_Prime_Project, Sub_Project, Sub_Project_Prime_Data, Sub_Project_Sub_Data, \
    File_For_Project, Comment_For_Project, File_For_Comment, Alarm, Incom, Incom_Data, Outcom, Outcom_Data, Contacts, Data_Contacts, \
    Status_Project, File_Incom_Data, File_Outcom_Data


class Inlines_Alarm (admin.TabularInline):
    model = Alarm
    extra = 0


class Inlines_File_For_Comment (admin.TabularInline):
    model = File_For_Comment
    extra = 0


class Inlines_Comment_For_Project (admin.TabularInline):
    model = Comment_For_Project
    extra = 0


class Inlines_File_For_Project (admin.TabularInline):
    model = File_For_Project
    extra = 0


class Inlines_Sub_Project_Sub_Data (admin.TabularInline):
    model = Sub_Project_Sub_Data
    extra = 0


class Inlines_Sub_Project_Prime_Data (admin.TabularInline):
    model = Sub_Project_Prime_Data
    extra = 0


class Inlines_Sub_Project (admin.TabularInline):
    model = Sub_Project
    extra = 0


class Inlines_Status_Project (admin.TabularInline):
    model = Status_Project
    extra = 0


class Inlines_Data_Prime_Project (admin.TabularInline):
    model = Data_Prime_Project
    extra = 0


class Inlines_Prime_Project (admin.TabularInline):
    model = Prime_Project
    extra = 0


class Inlines_Incom (admin.TabularInline):
    model = Incom
    extra = 0


class Inlines_Incom_Data (admin.TabularInline):
    model = Incom_Data
    extra = 0


class Inlines_File_Incom_Data (admin.TabularInline):
    model = File_Incom_Data
    extra = 0


class Inlines_Outcom (admin.TabularInline):
    model = Outcom
    extra = 0

class Inlines_Outcom_Data (admin.TabularInline):
    model = Outcom_Data
    extra = 0


class Inlines_File_Outcom_Data (admin.TabularInline):
    model = File_Outcom_Data
    extra = 0


class Inlines_Contacts (admin.TabularInline):
    model = Contacts
    extra = 0


class Inlines_Data_Contacts (admin.TabularInline):
    model = Data_Contacts
    extra = 0


class Admin_Prime_Project (admin.ModelAdmin):
    list_display = [field.name for field in Prime_Project._meta.fields]
    inlines = [Inlines_Alarm, Inlines_Data_Prime_Project, Inlines_File_For_Project, Inlines_Sub_Project, Inlines_Comment_For_Project,
               Inlines_Contacts, Inlines_Status_Project, Inlines_Incom, Inlines_Outcom]

    class Meta:
        model = Prime_Project

admin.site.register(Prime_Project, Admin_Prime_Project)


class Admin_Data_Prime_Project (admin.ModelAdmin):
    list_display = [field.name for field in Data_Prime_Project._meta.fields]

    class Meta:
        model = Data_Prime_Project

admin.site.register(Data_Prime_Project, Admin_Data_Prime_Project)


class Admin_Status_Project (admin.ModelAdmin):
    list_display = [field.name for field in Status_Project._meta.fields]

    class Meta:
        model = Status_Project

admin.site.register(Status_Project, Admin_Status_Project)


class Admin_Sub_Project (admin.ModelAdmin):
    list_display = [field.name for field in Sub_Project._meta.fields]
    inlines = [Inlines_Alarm, Inlines_Sub_Project_Sub_Data, Inlines_Sub_Project_Prime_Data]

    class Meta:
        model = Sub_Project

admin.site.register(Sub_Project, Admin_Sub_Project)


class Admin_Sub_Project_Prime_Data (admin.ModelAdmin):
    list_display = [field.name for field in Sub_Project_Prime_Data._meta.fields]
    inlines = [Inlines_Sub_Project_Sub_Data]

    class Meta:
        model = Sub_Project_Prime_Data

admin.site.register(Sub_Project_Prime_Data, Admin_Sub_Project_Prime_Data)


class Admin_Incom (admin.ModelAdmin):
    list_display = [field.name for field in Incom._meta.fields]
    inlines = [Inlines_Incom_Data]

    class Meta:
        model = Incom

admin.site.register(Incom, Admin_Incom)


class Admin_Incom_Data (admin.ModelAdmin):
    list_display = [field.name for field in Incom_Data._meta.fields]
    inlines = [Inlines_File_Incom_Data]

    class Meta:
        model = Incom_Data

admin.site.register(Incom_Data, Admin_Incom_Data)


class Admin_File_Incom_Data (admin.ModelAdmin):
    list_display = [field.name for field in File_Incom_Data._meta.fields]

    class Meta:
        model = File_Incom_Data

admin.site.register(File_Incom_Data, Admin_File_Incom_Data)


class Admin_Outcom (admin.ModelAdmin):
    list_display = [field.name for field in Outcom._meta.fields]
    inlines = [Inlines_Outcom_Data]

    class Meta:
        model = Outcom

admin.site.register(Outcom, Admin_Outcom)


class Admin_Outcom_Data (admin.ModelAdmin):
    list_display = [field.name for field in Outcom_Data._meta.fields]
    inlines = [Inlines_File_Outcom_Data]

    class Meta:
        model = Outcom_Data

admin.site.register(Outcom_Data, Admin_Outcom_Data)



class Admin_File_Outcom_Data (admin.ModelAdmin):
    list_display = [field.name for field in File_Outcom_Data._meta.fields]

    class Meta:
        model = File_Outcom_Data

admin.site.register(File_Outcom_Data, Admin_File_Outcom_Data)


class Admin_Sub_Project_Sub_Data (admin.ModelAdmin):
    list_display = [field.name for field in Sub_Project_Sub_Data._meta.fields]
    inlines = []

    class Meta:
        model = Sub_Project_Sub_Data

admin.site.register(Sub_Project_Sub_Data, Admin_Sub_Project_Sub_Data)


class Admin_File_For_Project (admin.ModelAdmin):
    list_display = [field.name for field in File_For_Project._meta.fields]
    inlines = []

    class Meta:
        model = File_For_Project

admin.site.register(File_For_Project, Admin_File_For_Project)


class Admin_Comment_For_Project (admin.ModelAdmin):
    list_display = [field.name for field in Comment_For_Project._meta.fields]
    inlines = [Inlines_File_For_Comment]

    class Meta:
        model = Comment_For_Project

admin.site.register(Comment_For_Project, Admin_Comment_For_Project)


class Admin_File_For_Comment (admin.ModelAdmin):
    list_display = [field.name for field in File_For_Comment._meta.fields]
    inlines = []

    class Meta:
        model = File_For_Comment

admin.site.register(File_For_Comment, Admin_File_For_Comment)


class Admin_Contacts (admin.ModelAdmin):
    list_display = [field.name for field in Contacts._meta.fields]
    inlines = [Inlines_Data_Contacts]

    class Meta:
        model = Contacts

admin.site.register(Contacts, Admin_Contacts)


class Admin_Data_Contacts (admin.ModelAdmin):
    list_display = [field.name for field in Data_Contacts._meta.fields]
    inlines = []

    class Meta:
        model = Data_Contacts

admin.site.register(Data_Contacts, Admin_Data_Contacts)



class Admin_Alarm (admin.ModelAdmin):
    list_display = [field.name for field in Alarm._meta.fields]
    inlines = []

    class Meta:
        model = Alarm

admin.site.register(Alarm, Admin_Alarm)

