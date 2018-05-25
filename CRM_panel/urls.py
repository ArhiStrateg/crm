from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^', include('main.urls')),
    url(r'^', include('projects.urls')),
    url(r'^', include('tasks.urls')),
    url(r'^', include('login.urls')),

] \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)