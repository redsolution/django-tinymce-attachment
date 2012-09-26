# -*- coding: utf-8 -*-

import os
from django.db import models
from imagekit.models import ImageModel
from attachment import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from attachment.fields import ImagePreviewField

class AttachmentImage(ImageModel):
    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
        ordering = ('position',)

    class IKOptions:
        spec_module = settings.ATTACHMENT_IKSPECS
        cache_dir = settings.ATTACHMENT_CACHE_DIR
        cache_filename_format = "%(filename)s-%(specname)s.%(extension)s"
        image_field = 'image'

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    image = ImagePreviewField(verbose_name=_('image'),
        upload_to=settings.ATTACHMENT_UPLOAD_DIR)
    
    position = models.IntegerField(verbose_name=_('position'),
        default=1, blank=False)
    
    title = models.CharField(verbose_name=_('title'),
        max_length=200, blank=True, null=True)

    group = models.CharField(verbose_name=_('group'),
        max_length=200, blank=True, null=True)

    def __unicode__(self):
        if self.image:
            return os.path.basename(self.image.url)
        else:
            return u''

class AttachmentFile(models.Model):
    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    file = models.FileField(verbose_name=_('file'), upload_to=settings.ATTACHMENT_UPLOAD_DIR)

    position = models.IntegerField(verbose_name=u'Порядок расположения', default=1, blank=False)

    title = models.CharField(verbose_name=_('title'), max_length=100,
        blank=True, null=True)

    def __unicode__(self):
        if self.file:
            return os.path.basename(self.file.url)
        else:
            return u''
