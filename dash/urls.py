from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns(
    '',
    url(r'^main/$', views.main, name='main'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^edit/$', views.edit_user, name='edit_user'),
    # url(r'^edit/(?P<pk>\d+)$', views.edit_user, name='edit_user'),
    url('^delete/$', views.delete_user, name='delete_user'),
)
