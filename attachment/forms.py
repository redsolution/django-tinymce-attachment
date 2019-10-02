# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import TextInput, Select
from django.core.exceptions import ValidationError
from attachment.models import AttachmentImage, AttachmentFile, AttachmentArchive
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from attachment import settings
from .widgets import ImagePreviewWidget, FileWidget


def validate_size(file, size):
    try:
        if size and file.size > size:
            error = _("File too large") + " ( > %s )" % (filesizeformat(size))
            raise ValidationError(error)
    except OSError:
        pass
    return file


class AttachmentImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AttachmentImageForm, self).__init__(*args, **kwargs)
        if settings.ATTACHMENT_IMAGE_ROLES:
            choices = [(role, role) for role in settings.ATTACHMENT_IMAGE_ROLES]
            self.fields["role"].widget.choices = [(None, '--------')] + choices

    class Meta:
        model = AttachmentImage
        fields = '__all__'
        widgets = {
            'title': TextInput,
            'image': ImagePreviewWidget,
            'role': Select
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        return validate_size(image, settings.ATTACHMENT_MAX_IMAGE_UPLOAD_SIZE)


class AttachmentFileForm(forms.ModelForm):

    class Meta:
        model = AttachmentFile
        fields = '__all__'
        widgets = {
            'title': TextInput,
            'file': FileWidget
        }

    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        return validate_size(file, settings.ATTACHMENT_MAX_FILE_UPLOAD_SIZE)


class AttachmentArchiveInlineForm(forms.ModelForm):
    class Meta:
        model = AttachmentArchive
        exclude = ['file_list', 'uploaded_date', 'unpacked']
