import os
from redsolutioncms.make import BaseMake
from redsolutioncms.models import CMSSettings
from attachment.redsolution_setup.models import AttachmentSettings

class Make(BaseMake):
    def make(self):
        super(Make, self).make()
        attachment_settings = AttachmentSettings.objects.get_settings()
        cms_settings = CMSSettings.objects.get_settings()
        cms_settings.render_to('urls.py', 'attachment/redsolutioncms/urls.pyt', {
            'attachment_settings': attachment_settings,
        })

    def postmake(self):
        super(Make, self).postmake()
        attachment_settings = AttachmentSettings.objects.get_settings()
        cms_settings = CMSSettings.objects.get_settings()
        cms_settings.render_to('settings.py', 'attachment/redsolutioncms/settings.pyt', {
            'attachment_settings': attachment_settings,
        })

make = Make()

