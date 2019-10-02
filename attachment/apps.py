# -*- encoding: utf-8 -*-
from django.apps import AppConfig


class AttachmentAppConfig(AppConfig):
    name = 'attachment'
    verbose_name = u'Архивы вложений'

    def ready(self):
        import attachment.signals
