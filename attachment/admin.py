# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.core.exceptions import ImproperlyConfigured
from attachment.importpath import importpath
from attachment.forms import AttachmentImageForm, AttachmentFileForm
from attachment.models import AttachmentImage, AttachmentFile
from attachment.settings import ATTACHMENT_EXTRA_IMAGES, ATTACHMENT_EXTRA_FILES, GROUP_IMAGES

class AttachmentImageInlines(generic.GenericStackedInline):
    class Meta:
        ordering = ('position',)
    
    model = AttachmentImage
    exclude = ('group',) if not GROUP_IMAGES else None
    form = AttachmentImageForm
    extra = ATTACHMENT_EXTRA_IMAGES

class AttachmentFileInlines(generic.GenericStackedInline):
    class Meta:
        ordering = ('position',)
    
    model = AttachmentFile
    form = AttachmentFileForm
    extra = ATTACHMENT_EXTRA_FILES

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
        model_admin.inlines = list(model_admin.inlines)[:] + [AttachmentImageInlines]
    if not AttachmentFileInlines in model_admin.inlines:
        model_admin.inlines = list(model_admin.inlines)[:] + [AttachmentFileInlines]

    admin.site.register(model, model_admin)
