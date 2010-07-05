# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.core.exceptions import ImproperlyConfigured
from attachment.importpath import importpath
from attachment.forms import AttachmentImageForm, AttachmentFileForm
from attachment.models import AttachmentImage, AttachmentFile

class AttachmentImageInlines(generic.GenericStackedInline):
    model = AttachmentImage
    form = AttachmentImageForm
    extra = 3

class AttachmentFileInlines(generic.GenericStackedInline):
    model = AttachmentFile
    form = AttachmentFileForm
    extra = 3

try:
    admin.site.register(AttachmentImage)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(AttachmentFile)
except admin.sites.AlreadyRegistered:
    pass

if not hasattr(settings, 'ATTACHMENT_FOR_MODELS'):
    raise ImproperlyConfigured('Please add ``ATTACHMENT_FOR_MODELS = ["<app>.models.<Model>",]`` to your settings.py')

for model_name in settings.ATTACHMENT_FOR_MODELS:
    model = importpath(model_name, 'ATTACHMENT_FOR_MODELS')
    try:
        model_admin = admin.site._registry[model].__class__
    except KeyError:
        raise ImproperlyConfigured('Please set ``attachment`` in your settings.py only as last INSTALLED_APPS')
    admin.site.unregister(model)

    setattr(model_admin, 'inlines', getattr(model_admin, 'inlines', []))
    if not AttachmentImageInlines in model_admin.inlines:
        model_admin.inlines.append(AttachmentImageInlines)
    if not AttachmentFileInlines in model_admin.inlines:
        model_admin.inlines.append(AttachmentFileInlines)

    admin.site.register(model, model_admin)
