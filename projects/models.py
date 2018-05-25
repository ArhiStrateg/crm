from django.db import models
from login.models import User_Login


class Prime_Project(models.Model):
    name_project = models.CharField(max_length=64, blank=True, null=True)
    description_project = models.CharField(max_length=256, blank=True, null=True)
    who_create_project = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    status_1 = models.BooleanField(default=False)
    status_2 = models.BooleanField(default=False)
    status_3 = models.BooleanField(default=False)
    status_4 = models.BooleanField(default=False)
    status_5 = models.BooleanField(default=False)
    status_6 = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Data_Prime_Project(models.Model):
    prime_project = models.ForeignKey(Prime_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)
    key_yacor_project = models.CharField(max_length=10, blank=True, null=True)
    who_boss_project = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    date_create_project = models.DateField(auto_now=True)
    date_start_project = models.DateField(blank=True, null=True)
    date_deadline_project = models.DateField(blank=True, null=True)
    date_fact_end = models.DateField(blank=True, null=True)
    archiv_project = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Информаци по проекту'
        verbose_name_plural = 'Информация по проектам'


class Status_Project(models.Model):
    boss_project = models.ForeignKey(Prime_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)

    date_create_start_status = models.DateField(auto_now=True)
    date_deadline_status = models.DateField(blank=True, null=True)
    date_fact_end_status = models.DateField(blank=True, null=True)

    who_resend_status = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    status_1 = models.BooleanField(default=False)
    status_2 = models.BooleanField(default=False)
    status_3 = models.BooleanField(default=False)
    status_4 = models.BooleanField(default=False)
    status_5 = models.BooleanField(default=False)
    status_6 = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Статус данные'
        verbose_name_plural = 'Статусы данные'


class Sub_Project(models.Model):
    name_project = models.CharField(max_length=64, blank=True, null=True)
    description_project = models.CharField(max_length=256, blank=True, null=True)
    prime_project = models.ForeignKey(Prime_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)
    who_create_project = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    pair = models.CharField(max_length=256, blank=True, null=True)
    map = models.CharField(max_length=256, blank=True, null=True)
    do_it = models.BooleanField(default=False)
    status_1 = models.BooleanField(default=False)
    status_2 = models.BooleanField(default=False)
    status_3 = models.BooleanField(default=False)
    status_4 = models.BooleanField(default=False)
    status_5 = models.BooleanField(default=False)
    status_6 = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Субпроект'
        verbose_name_plural = 'Субпроекты'


class Sub_Project_Prime_Data(models.Model):
    local_key = models.ForeignKey(Sub_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)
    who_boss_project = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    key_yacor_project = models.CharField(max_length=64, blank=True, null=True)
    level_project = models.IntegerField()
    date_create_project = models.DateField(auto_now=True)
    date_start_project = models.DateField(blank=True, null=True)
    date_deadline_project = models.DateField(blank=True, null=True)
    date_fact_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Информация по субпроекту'
        verbose_name_plural = 'Информация по субпроектам'


class Sub_Project_Sub_Data(models.Model):
    local_key = models.ForeignKey(Sub_Project_Prime_Data, blank=True, null=True, default=None, on_delete=models.CASCADE)
    boss_key = models.ForeignKey(Sub_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Дополнительная информация по субпроекту'
        verbose_name_plural = 'Дополнительная информация по субпроектам'


class Comment_For_Project(models.Model):
    text_comment = models.CharField(max_length=256, blank=True, null=True)
    who_create = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    boss_project = models.ForeignKey(Prime_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now=True)
    status_1 = models.BooleanField(default=False)
    status_2 = models.BooleanField(default=False)
    status_3 = models.BooleanField(default=False)
    status_4 = models.BooleanField(default=False)
    status_5 = models.BooleanField(default=False)
    status_6 = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Комментарий по проекту'
        verbose_name_plural = 'Комментарии по проектам'


class File_For_Comment(models.Model):
    file = models.FileField(upload_to='file_atach_comment/', blank=True, null=True, default=None)
    boss_comment = models.ForeignKey(Comment_For_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Прикрепленный файл к комментарию'
        verbose_name_plural = 'Прикрепленные файлы к комментариям'


class Comment_For_Sub_Project(models.Model):
    text_comment = models.CharField(max_length=256, blank=True, null=True)
    who_create = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    boss_project = models.ForeignKey(Sub_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Комментарий по подпроекту'
        verbose_name_plural = 'Комментарии по подпроектам'


class File_For_Project(models.Model):
    file = models.FileField(upload_to='file_atach_project/', blank=True, null=True, default=None)
    description_file = models.CharField(max_length=256, blank=True, null=True)
    boss_project = models.ForeignKey(Prime_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)
    who_create = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Прикрепленный файл к проекту'
        verbose_name_plural = 'Прикрепленные файлы к проекту'


class Alarm(models.Model):
    prime_project = models.ForeignKey(Prime_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)
    boss_project = models.ForeignKey(Sub_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)
    alarm_true = models.BooleanField(default=False)
    alarm_off = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'ДЕДЛАЙН'
        verbose_name_plural = 'ДЕДЛАЙНы'


class Incom(models.Model):
    project = models.ForeignKey(Prime_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)
    inc_project = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=None)
    description = models.CharField(max_length=256, blank=True, null=True)
    who_create = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now=True)
    status_1 = models.BooleanField(default=False)
    status_2 = models.BooleanField(default=False)
    status_3 = models.BooleanField(default=False)
    status_4 = models.BooleanField(default=False)
    status_5 = models.BooleanField(default=False)
    status_6 = models.BooleanField(default=False)


    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Доход'
        verbose_name_plural = 'Доходы'


class Incom_Data(models.Model):
    local_key = models.ForeignKey(Incom, blank=True, null=True, default=None, on_delete=models.CASCADE)
    who_update = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    date_update = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Дополнительная информация о доходах'
        verbose_name_plural = 'Дополнительная информация о доходах'


class File_Incom_Data(models.Model):
    local_key = models.ForeignKey(Incom_Data, blank=True, null=True, default=None, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file_atach_project_incom/', blank=True, null=True, default=None)
    description_file = models.CharField(max_length=256, blank=True, null=True)
    who_create = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Прикрепленный файл к доходу'
        verbose_name_plural = 'Прикрепленные файлы к доходам'


class Outcom(models.Model):
    project = models.ForeignKey(Prime_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)
    inc_project = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=None)
    description = models.CharField(max_length=256, blank=True, null=True)
    who_create = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now=True)
    status_1 = models.BooleanField(default=False)
    status_2 = models.BooleanField(default=False)
    status_3 = models.BooleanField(default=False)
    status_4 = models.BooleanField(default=False)
    status_5 = models.BooleanField(default=False)
    status_6 = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'


class Outcom_Data(models.Model):
    local_key = models.ForeignKey(Outcom, blank=True, null=True, default=None, on_delete=models.CASCADE)
    who_update = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    date_update = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Дополнительная информация о расходах'
        verbose_name_plural = 'Дополнительная информация о расходах'


class File_Outcom_Data(models.Model):
    local_key = models.ForeignKey(Outcom_Data, blank=True, null=True, default=None, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file_atach_project_outcom/', blank=True, null=True, default=None)
    description_file = models.CharField(max_length=256, blank=True, null=True)
    who_create = models.ForeignKey(User_Login, blank=True, null=True, default=None, on_delete=models.CASCADE)
    date_create = models.DateField(auto_now=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Прикрепленный файл к расходу'
        verbose_name_plural = 'Прикрепленные файлы к расходам'


class Contacts(models.Model):
    prime_project = models.ForeignKey(Prime_Project, blank=True, null=True, default=None, on_delete=models.CASCADE)
    name_company = models.CharField(max_length=64, blank=True, null=True)
    phone_company = models.CharField(max_length=64, blank=True, null=True)
    location_company = models.CharField(max_length=64, blank=True, null=True)
    site_company = models.CharField(max_length=50, blank=True, null=True)
    mail_company = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Контактные данные'
        verbose_name_plural = 'Контактные данные'


class Data_Contacts(models.Model):
    local_key = models.ForeignKey(Contacts, blank=True, null=True, default=None, on_delete=models.CASCADE)
    fio_client = models.CharField(max_length=64, blank=True, null=True)
    doljnost = models.CharField(max_length=50, blank=True, null=True)
    phone_client = models.CharField(max_length=50, blank=True, null=True)
    mail_client = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Дополнительная информация к контактным данным'
        verbose_name_plural = 'Дополнительная информация к контактным данным'
