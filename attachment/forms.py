# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError
from attachment.models import AttachmentImage, AttachmentFile
from attachment.settings import ATTACHMENT_MAX_LENGTH_DIFF, ATTACHMENT_MAX_IMAGE_UPLOAD_SIZE, ATTACHMENT_MAX_FILE_UPLOAD_SIZE
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


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
        self.fields['image'].max_length -= ATTACHMENT_MAX_LENGTH_DIFF
    class Meta:
        model = AttachmentImage
        fields = '__all__'
        widgets = {
            'title': TextInput(),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        return validate_size(image, ATTACHMENT_MAX_IMAGE_UPLOAD_SIZE)


class AttachmentFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AttachmentFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].max_length -= ATTACHMENT_MAX_LENGTH_DIFF
    class Meta:
        model = AttachmentFile
        fields = '__all__'
        widgets = {
            'title': TextInput(),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        return validate_size(file, ATTACHMENT_MAX_FILE_UPLOAD_SIZE)
