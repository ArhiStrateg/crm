from django.conf.urls import url
from projects.views import projects, create_new_project, project, create_new_subproject, create_new_subproject_low, upd_project,\
    int_sub_project, upd_sub_project, finacial, finaciar

urlpatterns = [

    url(r'^projects/$', projects, name='projects'),
    url(r'^project/(?P<project_id>\w+)/$', project, name='project'),
    url(r'^finacial/(?P<project_id>\w+)/$', finacial, name='finacial'),
    url(r'^finaciar/(?P<project_id>\w+)/$', finaciar, name='finaciar'),
    url(r'^create_new_project/$', create_new_project, name='create_new_project'),
    url(r'^upd_project/(?P<upd_project_id>\w+)/$', upd_project, name='upd_project'),

    url(r'^create_new_subproject/(?P<create_new_subproject_id>\w+)/$', create_new_subproject, name='create_new_subproject'),
    url(r'^create_new_subproject_low/(?P<create_new_subproject_low_id>\w+)/$', create_new_subproject_low, name='create_new_subproject_low'),
    url(r'^int_sub_project/(?P<int_sub_project_id>\w+)/$', int_sub_project, name='int_sub_project'),
    url(r'^upd_sub_project/(?P<upd_sub_project_id>\w+)/$', upd_sub_project, name='upd_sub_project'),

]
