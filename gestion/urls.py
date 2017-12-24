from django.conf.urls import url
from . import views

app_name = 'gestion'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<companie_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<employee_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^employees/(?P<filter_by>[a-zA_Z]+)/$', views.employees, name='employees'),
    url(r'^create_companie/$', views.create_companie, name='create_companie'),
    url(r'^(?P<companie_id>[0-9]+)/create_employee/$', views.create_employee, name='create_employee'),
    url(r'^(?P<companie_id>[0-9]+)/delete_employee/(?P<employee_id>[0-9]+)/$', views.delete_employee, name='delete_employee'),
    url(r'^(?P<companie_id>[0-9]+)/favorite_companie/$', views.favorite_companie, name='favorite_companie'),
    url(r'^(?P<companie_id>[0-9]+)/delete_companie/$', views.delete_companie, name='delete_companie'),
]
