# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import links, images

urlpatterns = [
    url(r'^admin/(?P<app_label>\w+)/(?P<module_name>\w+)/(?P<object_id>\d{1,7})/change/images/change/$', images),
    url(r'^admin/(?P<app_label>\w+)/(?P<module_name>\w+)/(?P<object_id>\d{1,7})/change/links/change/$', links),
    url(r'^admin/(?P<app_label>\w+)/(?P<module_name>\w+)/(?P<object_id>\d{1,7})/images/$', images),
    url(r'^admin/(?P<app_label>\w+)/(?P<module_name>\w+)/(?P<object_id>\d{1,7})/links/$', links),
    url(r'^admin/(?P<app_label>\w+)/(?P<module_name>\w+)/add/images/$', images),
    url(r'^admin/(?P<app_label>\w+)/(?P<module_name>\w+)/add/links/$', links),
]
