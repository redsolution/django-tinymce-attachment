# -*- coding: utf-8 -*-

from django import forms
from attachment.models import AttachmentImage, AttachmentFile
from attachment.widgets import ImageAdminWidget

class AttachmentImageForm(forms.ModelForm):
    class Meta:
        model = AttachmentImage

    image = forms.ImageField(
        required=not AttachmentImage._meta.get_field('image').blank,
        widget=ImageAdminWidget,
        label=AttachmentImage._meta.get_field('image').verbose_name,
        initial=AttachmentImage._meta.get_field('image').default,
        help_text=AttachmentImage._meta.get_field('image').help_text,
    )

class AttachmentFileForm(forms.ModelForm):
    class Meta:
        model = AttachmentFile
