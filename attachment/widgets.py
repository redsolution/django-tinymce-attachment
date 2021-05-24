# -*- coding: utf-8 -*-
import re
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_text
from unidecode import unidecode
from django.forms.widgets import FILE_INPUT_CONTRADICTION, CheckboxInput, ClearableFileInput


class ImagePreviewWidget(AdminFileWidget):

    template_name = 'admin/attachment/widgets/preview_image_input.html'

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        output.append(super(AdminFileWidget, self).render(name, value, attrs)) # really for AdminFileWidget
        instance = getattr(value, 'instance', None)
        if instance is not None and value:
            output = ['<a target="_blank" href="%s"><img src="%s" alt="%s"/></a>' % \
                (instance.image.url, instance.thumb.url, instance.image)] + output
        return mark_safe(u''.join(output))

    def value_from_datadict(self, data, files, name):

        for key, file in files.items():
            filename = file._get_name()
            ext = u""
            if '.' in filename:
                ext = u"." + filename.rpartition('.')[2]
            filename = filename.rpartition('.')[0]
            filename = re.sub(r'[_.,:;@#$%^&?*|()\[\]]', '-', filename)
            filename = slugify(unidecode(smart_text(filename))) + ext
            files[key]._set_name(filename)

        upload = super(ImagePreviewWidget, self).value_from_datadict(data, files, name)
        if not self.is_required and CheckboxInput().value_from_datadict(
                data, files, self.clear_checkbox_name(name)):

            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # object that FileField will turn into a ValidationError.
                return FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value, as opposed to just None
            return False
        return upload


class ImagePreviewWidgetHorizontal(ImagePreviewWidget):

    template_name = 'admin/attachment/widgets/preview_image_input_horizontal.html'


class ImagePreviewWidgetVertical(ImagePreviewWidget):

    template_name = 'admin/attachment/widgets/preview_image_input_vertical.html'


class FileWidget(ClearableFileInput):

    def value_from_datadict(self, data, files, name):
        for key, file in files.items():
            filename = file._get_name()
            ext = u""
            if '.' in filename:
                ext = u"." + filename.rpartition('.')[2]
            filename = filename.rpartition('.')[0]
            filename = re.sub(r'[_.,:;@#$%^&?*|()\[\]]', '-', filename)
            filename = slugify(unidecode(smart_text(filename))) + ext
            files[key]._set_name(filename)

        return files.get(name, None)
