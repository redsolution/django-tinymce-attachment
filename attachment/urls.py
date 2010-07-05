# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^admin/(?P<app_label>\w+)/(?P<module_name>\w+)/(?P<object_id>\d{1,7})/images/$', 'attachment.views.images'),
    url(r'^admin/(?P<app_label>\w+)/(?P<module_name>\w+)/(?P<object_id>\d{1,7})/links/$', 'attachment.views.links'),
    url(r'^admin/(?P<app_label>\w+)/(?P<module_name>\w+)/add/images/$', 'attachment.views.images'),
    url(r'^admin/(?P<app_label>\w+)/(?P<module_name>\w+)/add/links/$', 'attachment.views.links'),
)
