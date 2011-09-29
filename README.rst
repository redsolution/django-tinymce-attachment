=========================
django-tinymce-attachment
=========================

django-tinymce-attachment.

Installation:
=============

1. Put ``attachment`` as LAST item to your ``INSTALLED_APPS`` in your ``settings.py`` within your Django project.

2. Sync your database ::

    ./manage.py syncdb

Usage:
======

In settings.py:
---------------

Specify Models for which you`d like to add images and files :: 
    
    ATTACHMENT_FOR_MODELS = [
        '<app>.models.<Model>',
    ]

Specify Model to be listed in link-list :: 
    
    ATTACHMENT_LINK_MODELS = [
        '<app>.models.<Model>',
    ]
    
For objects listed in link-list these attributes will be used:

- ``get_absolute_url()`` to retrieve url.
- ``__unicode()__`` to retrieve verbose name.

In urls.py:
-----------

Add attachment to urls.py BEFORE ``admin/`` ::

    (r'^', include('attachment.urls')), # Must be placed before admin/


Example:
========

``settings.py`` ::

    INSTALLED_APPS = (
        ...
        'attachment',
    )
    
    ATTACHMENT_FOR_MODELS = [
        'item.models.Item',
    ]

    ATTACHMENT_LINK_MODELS = [
        'news.models.News',
    ]
    
    TINYMCE_DEFAULT_CONFIG = {
        'external_image_list_url': 'images/',
        'external_link_list_url': 'links/',
    }
    
``urls.py`` ::

    urlpatterns += patterns('',
        (r'^', include('attachment.urls')), # Must be placed before admin/
        (r'^admin/', include(admin.site.urls)),
    )
        
Now you can attach images and files to Item object.
After you will save Item-object in TinyMCE editor for this page will be available:

- attached images in list of images.
- attached files in list of links.
- all News objects in list of links.

Here are screenshots that demonstrates attachment work:

* |Link list| - link lists
* |Image list| - image lists
* |Attached files| - attached files

Changelog:
----------

* 0.2.0 - Add field "title" for models AttachmentFile, AttachmentImage
* 0.3.0 - Ordering by new "position" field enabled.

Classifiers:
-------------

`Content plugins`_

.. _`Content plugins`: http://www.redsolutioncms.org/classifiers/content
.. |Link list| image:: http://github.com/redsolution/django-tinymce-attachment/raw/0.1.0/doc/link-list.png
.. |Image list| image:: http://github.com/redsolution/django-tinymce-attachment/raw/0.1.0/doc/image-list.png
.. |Attached files| image:: http://github.com/redsolution/django-tinymce-attachment/raw/0.1.0/doc/attachments.png
