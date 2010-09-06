from django.contrib import admin
from attachment.redsolution_setup.models import AttachmentSettings, AttachmentModel, AttachmentLink

class AttachmentModelInline(admin.TabularInline):
    model = AttachmentModel

class AttachmentLinkInline(admin.TabularInline):
    model = AttachmentLink

class AttachmentSettingsForm(admin.ModelAdmin):
    model = AttachmentSettings
    inlines = [AttachmentModelInline, AttachmentLinkInline]

try:
    admin.site.register(AttachmentSettings, AttachmentSettingsForm)
except admin.sites.AlreadyRegistered:
    pass
