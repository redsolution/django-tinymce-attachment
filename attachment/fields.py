# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from attachment.widgets import ImagePreviewWidget
from django.contrib.admin.widgets import AdminFileWidget

class ImagePreviewFormField(forms.ImageField):
    widget = ImagePreviewWidget

class ImagePreviewField(models.ImageField):
    def formfield(self, **kwargs):
        defaults = {'widget': ImagePreviewWidget}
        defaults.update(kwargs)

        # As an ugly hack, we override the admin widget
        if defaults['widget'] == AdminFileWidget:
            defaults['widget'] = ImagePreviewWidget

        return super(ImagePreviewField, self).formfield(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^attachment\.fields\.ImagePreviewField"])
except ImportError:
    pass
