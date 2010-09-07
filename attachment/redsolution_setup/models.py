# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from redsolutioncms.models import BaseSettings

class AttachmentSettings(BaseSettings):
    pass

class AttachmentModel(models.Model):
    settings = models.ForeignKey(AttachmentSettings, related_name='models')
    model = models.CharField(verbose_name=_('Mode'), max_length=255)

class AttachmentLink(models.Model):
    settings = models.ForeignKey(AttachmentSettings, related_name='links')
    model = models.CharField(verbose_name=_('Mode'), max_length=255)
