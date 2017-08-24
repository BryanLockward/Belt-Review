from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register),
    url(r'^user/(?P<user_id>\d+)$', views.show)
]
