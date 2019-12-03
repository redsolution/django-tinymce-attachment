# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.core.exceptions import ImproperlyConfigured

from .importpath import importpath
from .forms import AttachmentImageForm, AttachmentFileForm, AttachmentArchiveInlineForm
from .models import AttachmentImage, AttachmentFile, AttachmentArchive
from .settings import ATTACHMENT_EXTRA_IMAGES, ATTACHMENT_EXTRA_FILES, GROUP_IMAGES, ATTACHMENT_IMAGE_ROLES


def get_excluded_fields():
    result = []
    if not ATTACHMENT_IMAGE_ROLES:
        result.append('role')
    if not GROUP_IMAGES:
        result.append('group')
    return result


class AttachmentImageInlines(GenericTabularInline):
    class Meta:
        ordering = ('position',)

    model = AttachmentImage
    exclude = get_excluded_fields()
    form = AttachmentImageForm
    extra = ATTACHMENT_EXTRA_IMAGES


class AttachmentFileInlines(GenericTabularInline):
    class Meta:
        ordering = ('position',)

    model = AttachmentFile
    form = AttachmentFileForm
    extra = ATTACHMENT_EXTRA_FILES


class AttachmentArchiveInlines(GenericStackedInline):

    model = AttachmentArchive
    form = AttachmentArchiveInlineForm
    extra = 1
    template = 'admin/attachment/stacked_add_only.html'


if not hasattr(settings, 'ATTACHMENT_FOR_MODELS'):
    raise ImproperlyConfigured('Please add ``ATTACHMENT_FOR_MODELS = ["<app>.models.<Model>",]`` to your settings.py')

for model_path in settings.ATTACHMENT_FOR_MODELS:

    model = importpath(model_path)
    try:
        model_admin = admin.site._registry[model].__class__
    except KeyError:
        raise ImproperlyConfigured('Please set ``attachment`` in your settings.py only as last INSTALLED_APPS')

    admin.site.unregister(model)
    setattr(model_admin, 'inlines', getattr(model_admin, 'inlines', []))

    if AttachmentImageInlines not in model_admin.inlines:
        model_admin.inlines = list(model_admin.inlines)[:] + [AttachmentImageInlines]

    if AttachmentFileInlines not in model_admin.inlines:
        model_admin.inlines = list(model_admin.inlines)[:] + [AttachmentFileInlines]

    if AttachmentArchiveInlines not in model_admin.inlines:
        model_admin.inlines = list(model_admin.inlines)[:] + [AttachmentArchiveInlines]

    admin.site.register(model, model_admin)
