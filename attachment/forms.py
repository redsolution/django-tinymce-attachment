# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import TextInput
from attachment.models import AttachmentImage, AttachmentFile
from attachment.settings import ATTACHMENT_MAX_LENGTH_DIFF

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
