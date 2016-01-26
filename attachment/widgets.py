# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget


class ImagePreviewWidget(AdminFileWidget):
    def __init__(self, thumb_field='thumb', thumb_size=None, *args, **kwargs):
        """
        ``thumb_field`` name of field with thumb image. If None will use image itself.
        ``thumb_size`` maximum (width, height) to be displayed. If None original size will be used.
        """
        self.thumb_field = thumb_field
        self.thumb_size = thumb_size
        super(ImagePreviewWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        output = []
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        instance = getattr(value, 'instance', None)
        if instance is not None:
            try:
                field = getattr(instance, value.field.name, None)
                if field:
                    if self.thumb_field is None:
                        thumb_field = field
                    else:
                        thumb_field = getattr(instance, self.thumb_field, None)
                    if self.thumb_size is None:
                        style = ''
                    else:
                        cur_width, cur_height = field.width, field.height
                        thumb_width, thumb_height = self.thumb_size
                        if not thumb_width is None and not thumb_height is None:
                            ratio = min(float(thumb_width) / cur_width,
                                        float(thumb_height) / cur_height)
                        else:
                            if thumb_width is None:
                                ratio = float(thumb_height) / cur_height
                            else:
                                ratio = float(thumb_width) / cur_width
                        new_size = (int(round(cur_width * ratio)), int(round(cur_height * ratio)))
                        if new_size[0] > cur_width or new_size[1] > cur_height:
                            new_size = self.thumb_size
                        style = 'style="width: %spx; height: %spx; "' % new_size
                    output.append('<br /><a target="_blank" href="%s"><img src="%s" alt="%s" %s/></a>' % \
                        (field.url, thumb_field.url, field, style))
            except IOError:
                output = ['<p class="errornote">' + _('File access error') + '</p>',] + output
        return mark_safe(u''.join(output))