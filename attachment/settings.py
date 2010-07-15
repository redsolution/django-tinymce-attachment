# -*- coding: utf-8 -*-

from django.conf import settings

ATTACHMENT_FOR_MODELS = getattr(settings, 'ATTACHMENT_FOR_MODELS', [])
ATTACHMENT_LINK_MODELS = getattr(settings, 'ATTACHMENT_LINK_MODELS', [])

ATTACHMENT_UPLOAD_DIR = getattr(settings, 'ATTACHMENT_UPLOAD_DIR', 'upload/attachment/source')
ATTACHMENT_CACHE_DIR = getattr(settings, 'ATTACHMENT_CACHE_DIR', 'upload/attachment/cache')
ATTACHMENT_IKSPECS = getattr(settings, 'ATTACHMENT_IKSPECS', 'attachment.ikspecs')
ATTACHMENT_LEVEL_INDICATOR = getattr(settings, 'ATTACHMENT_LEVEL_INDICATOR', u'\u00A0\u00A0\u00A0')
