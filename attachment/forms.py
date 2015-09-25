# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import TextInput
from attachment.models import AttachmentImage, AttachmentFile


class AttachmentImageForm(forms.ModelForm):
    class Meta:
        model = AttachmentImage
        fields = '__all__'
        widgets = {
            'title': TextInput(),
        }


class AttachmentFileForm(forms.ModelForm):
    class Meta:
        model = AttachmentFile
        fields = '__all__'
        widgets = {
            'title': TextInput(),
        }
