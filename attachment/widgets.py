# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget

class ImagePreviewWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        output.append(super(AdminFileWidget, self).render(name, value, attrs)) # really for AdminFileWidget
        instance = getattr(value, 'instance', None)
        if instance is not None:
            output.append('<br /><a target="_blank" href="%s"><img src="%s" alt="%s" /></a>' % \
                (instance.image.url, instance.thumb.url, instance.image))
        return mark_safe(u''.join(output))
