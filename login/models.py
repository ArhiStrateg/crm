from django.db import models


# class Status_User(models.Model)

class User_Login(models.Model):
    name_login = models.CharField(max_length=64, blank=True, null=True)
    password_login = models.CharField(max_length=64, blank=True, null=True)
    is_active_login = models.BooleanField(default=True)
    session_key_login = models.CharField(max_length=124, blank=True, null=True, default=None)

    name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    surname = models.CharField(max_length=64, blank=True, null=True)

    session_key_login = models.CharField(max_length=124, blank=True, null=True, default=None)
    updated_login = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Пользователь для входа'
        verbose_name_plural = 'Пользователи для входа'


# class IP_True(models.Model):
#     name_user = models.ForeignKey(User_Login, blank=True, null=True, default=None)
#     true_ip = models.CharField(max_length=25, blank=True, null=True)
#
#     def __str__(self):
#         return "%s" % self.id
#
#     class Meta:
#         verbose_name = 'Список разрешенных IP'
#         verbose_name_plural = 'Списоки разрешенных IP'
#
#
# class MAC_True(models.Model):
#     name_user = models.ForeignKey(User_Login, blank=True, null=True, default=None)
#     true_mac = models.CharField(max_length=25, blank=True, null=True)
#
#     def __str__(self):
#         return "%s" % self.id
#
#     class Meta:
#         verbose_name = 'Список разрешенных MAC'
#         verbose_name_plural = 'Списоки разрешенных MAC'