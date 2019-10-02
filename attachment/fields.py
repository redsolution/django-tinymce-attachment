# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from attachment.widgets import ImagePreviewWidget, ImagePreviewWidgetHorizontal, ImagePreviewWidgetVertical


class ImagePreviewFormField(forms.ImageField):
    widget = ImagePreviewWidget


class ImagePreviewField(models.ImageField):

    def __init__(self, *args, **kwargs):
        widget_type = kwargs.get('widget_type')
        if widget_type:
            if widget_type == 'horizontal':
                self.widget = ImagePreviewWidgetHorizontal
            elif widget_type == 'vertial':
                self.widget = ImagePreviewWidgetVertical
            kwargs.pop('widget_type')
        else:
            self.widget = ImagePreviewWidget
        super(ImagePreviewField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {}
        defaults.update(kwargs)
        defaults['widget'] = self.widget
        return super(ImagePreviewField, self).formfield(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^attachment\.fields\.ImagePreviewField"])
except ImportError:
    pass
