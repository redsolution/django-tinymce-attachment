# -*- coding: utf-8 -*-

from django import forms
from attachment.models import AttachmentImage, AttachmentFile

class AttachmentImageForm(forms.ModelForm):
    class Meta:
        model = AttachmentImage

class AttachmentFileForm(forms.ModelForm):
    class Meta:
        model = AttachmentFile
