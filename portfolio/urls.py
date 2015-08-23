from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from dash import views

urlpatterns = patterns(
    '',
    url(r'^$', views.main, name='main'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dash/', include('dash.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
