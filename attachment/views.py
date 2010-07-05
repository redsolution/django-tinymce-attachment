# -*- coding: utf-8 -*-

import os
from django.http import Http404
from django.shortcuts import get_object_or_404
from tinymce.views import render_to_image_list, render_to_link_list
from attachment import settings
from attachment.importpath import importpath
from attachment.models import AttachmentImage, AttachmentFile
from django.contrib.contenttypes.models import ContentType

def get_object(app_label, module_name, object_id=None):
    """
    Get object by app_label, module_name and object_id.
    
    Return None specified model exists and object_id is None.
    
    Raise Http404 if specified model or object doesn`t exists.
    """
    for check in [importpath(model_name)
            for model_name in settings.ATTACHMENT_FOR_MODELS]:
        if app_label == check._meta.app_label and module_name == check._meta.module_name:
            model = check
            break
    else:
        raise Http404

    if object_id is None:
        return None
    else:
        return get_object_or_404(model, id=object_id)

def images(request, app_label, module_name, object_id=None):
    object = get_object(app_label, module_name, object_id)
    if object is None:
        images = []
    else:
        images = AttachmentImage.objects.filter(
            content_type=ContentType.objects.get_for_model(
                    object.__class__),
            object_id=object.id)
    link_list = [(os.path.basename(obj.image.url), obj.display.url) for obj in images]
    return render_to_image_list(link_list)

def links(request, app_label, module_name, object_id=None):
    try:
        object = get_object(app_label, module_name, object_id)
    except Http404:
        object = None

    if object is None:
        files = []
    else:
        files = AttachmentFile.objects.filter(
            content_type=ContentType.objects.get_for_model(
                    object.__class__),
            object_id=object.id)
    link_list = [(os.path.basename(obj.file.url), obj.file.url) for obj in files]

    for model_name in settings.ATTACHMENT_LINK_MODELS:
        model = importpath(model_name)
        for obj in model.objects.all():
            if hasattr(obj._meta, 'level_attr'): # Object support mptt
                prefix = settings.ATTACHMENT_LEVEL_INDICATOR * getattr(
                    obj, obj._meta.level_attr)
            else:
                prefix = ''
            link_list.append((u'%s%s' % (prefix, unicode(obj)), obj.get_absolute_url()))
    return render_to_link_list(link_list)
