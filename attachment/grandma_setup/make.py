import os
from grandma.make import BaseMake
from grandma.models import GrandmaSettings
from attachment.grandma_setup.models import AttachmentSettings

class Make(BaseMake):
    def make(self):
        super(Make, self).make()
        attachment_settings = AttachmentSettings.objects.get_settings()
        grandma_settings = GrandmaSettings.objects.get_settings()
        grandma_settings.render_to('urls.py', 'attachment/grandma/urls.py', {
            'urls_settings': urls_settings,
        })

    def postmake(self):
        super(Make, self).make()
        attachment_settings = AttachmentSettings.objects.get_settings()
        grandma_settings = GrandmaSettings.objects.get_settings()
        grandma_settings.render_to('settings.py', 'attachment/grandma/settings.py', {
            'attachment_settings': attachment_settings,
        })
