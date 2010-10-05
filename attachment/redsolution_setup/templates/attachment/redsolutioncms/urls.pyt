# --- django-tinymce-attachment ---

urlpatterns = patterns('',
    (r'^', include('attachment.urls')),
) + urlpatterns
