# django-tinymce-attachment
urlpatterns = patterns('',
    (r'^', include('attachment.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
) + urlpatterns
