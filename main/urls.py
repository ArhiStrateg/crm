from django.conf.urls import url
from main.views import main


urlpatterns = [

    url(r'^main/$', main, name='main'),

]
