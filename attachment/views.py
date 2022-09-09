# -*- coding: utf-8 -*-
import os
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from tinymce.views import render_to_image_list, render_to_link_list
from attachment import settings
from .importpath import importpath
from .models import AttachmentImage, AttachmentFile


def get_object(app_label, module_name, object_id=None):
    """
    Get object by app_label, module_name and object_id.
    Return None specified model exists and object_id is None.
    Raise Http404 if specified model or object doesn`t exists.
    """
    for check in [importpath(model_name)
        for model_name in settings.ATTACHMENT_FOR_MODELS]:
            if app_label == check._meta.app_label and module_name == check._meta.model_name:
                model = check
                break

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
            content_type=ContentType.objects.get_for_model(object.__class__),
            object_id=object.id
        )

    link_list = []
    for obj in images:
        link_list.append([os.path.basename(obj.image.url), obj.display.url])
        for spec in settings.ATTACHMENT_SPECS_FOR_TINYMCE:
            try:
                img = getattr(obj, spec)
            except AttributeError:
                pass
            else:
                link_list.append([os.path.basename(img.url), img.url])

    return render_to_image_list(link_list)


def links(request, app_label, module_name, object_id=None):
    try:
        object = get_object(app_label, module_name, object_id)
    except Http404:
        object = None

    if object is None:
        files = []
        images = []
    else:
        files = AttachmentFile.objects.filter(
            content_type=ContentType.objects.get_for_model(object.__class__),
            object_id=object.id
        )
        images = AttachmentImage.objects.filter(
            content_type=ContentType.objects.get_for_model(object.__class__),
            object_id=object.id
        )
    link_list = [(os.path.basename(obj.file.url), obj.file.url) for obj in files]

    for obj in images:
        link_list.append([os.path.basename(obj.image.url), obj.display.url])
        for spec in settings.ATTACHMENT_SPECS_FOR_TINYMCE:
            try:
                img = getattr(obj, spec)
            except AttributeError:
                pass
            else:
                link_list.append([os.path.basename(img.url), img.url])

    for model_name in settings.ATTACHMENT_LINK_MODELS:
        model = importpath(model_name)
        for obj in model.objects.all():
            if hasattr(obj._meta, 'level_attr'): # Object support mptt
                prefix = settings.ATTACHMENT_LEVEL_INDICATOR * getattr(
                    obj, obj._meta.level_attr)
            else:
                prefix = ''
            try:
                url = obj.get_absolute_url()
            except AttributeError:
                url = '/'
            link_list.append((u'%s%s' % (prefix, str(obj)), url))
    return render_to_link_list(link_list)
