import os
from redsolution.make import BaseMake
from redsolution.models import RedsolutionSettings
from attachment.redsolution_setup.models import AttachmentSettings

class Make(BaseMake):
    def make(self):
        super(Make, self).make()
        attachment_settings = AttachmentSettings.objects.get_settings()
        redsolution_settings = RedsolutionSettings.objects.get_settings()
        redsolution_settings.render_to('urls.py', 'attachment/redsolution/urls.py', {
            'attachment_settings': attachment_settings,
        })

    def postmake(self):
        super(Make, self).postmake()
        attachment_settings = AttachmentSettings.objects.get_settings()
        redsolution_settings = RedsolutionSettings.objects.get_settings()
        redsolution_settings.render_to('settings.py', 'attachment/redsolution/settings.pyt', {
            'attachment_settings': attachment_settings,
        })
