=========================
django-tinymce-attachment
=========================

django-tinymce-attachment.

Installation:
=============

1. Put ``attachment`` as LAST item to your ``INSTALLED_APPS`` in your ``settings.py`` within your django project.

2. Sync your database::

    ./manage.py syncdb

Usage:
======

In settings.py:
---------------

Specify Models for witch you`d like to add images and files:: 
    ATTACHMENT_FOR_MODELS = [
        '<app>.models.<Model>',
    ]

Specify Model to be listed in link-list:: 
    ATTACHMENT_LINK_MODELS = [
        '<app>.models.<Model>',
    ]
    
For objects to be listed in link-list will be called:

# ``get_absolute_url()`` to retrieve url.
# ``__unicode()__`` to retrieve verbose name.

In urls.py:
-----------

Add attachment to urls.py BEFORE ``admin/``::
        (r'^', include('attachment.urls')), # Must be placed before admin/


In template:
------------

Also you can get list of attachments in your templates.
First of all, load the attachment_tags in every template you want to use it::

    {% load attachment_tags %}

Use::
    {% show_<attachments|images|files> for <object> %}

Or::
    {% get_<attachments|images|files> for <object> as <variable> %}
    {% for attachment in <variable> %}
        {{ attachment.file }}
    {% endfor %}


Example:
========

``settings.py``::
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
    
``urls.py``::
    urlpatterns += patterns('',
        (r'^', include('attachment.urls')), # Must be placed before admin/
        (r'^admin/', include(admin.site.urls)),
    )

``templates/object.html``::
    {% load attachment_tags %}
    <html>
        <body>
            {% get_attachments for object as attachments %}
			<ul>
			    {% for attachment in attachments %}
			        {% if attachment.image %}
			            <li><a href="{{ attachment.image.url }}"><img src="{{ attachment.thumb.url }}" /></a></li>
			        {% else %}
			            <li><a href="{{ attachment.file.url }}">{{ attachment.file.url }}</a></li>
			        {% endif %}
			    {% endfor %}
			</ul>
        </body>
    </html>
        

Now you can attach images and files to Item-object.
After you will save Item-object in TinyMCE editor for this page will be available:

# attached images in list of images.
# attached files in list of links.
# all News objects in list of links.
