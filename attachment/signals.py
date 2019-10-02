from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import AttachmentArchive
from .utils import ZipExtractor


@receiver(post_save, sender=AttachmentArchive)
def create_attachments_from_archive(sender, **kwargs):
    instance = kwargs.get('instance')
    if not instance.unpacked:
        ZipExtractor(instance).make_attachments()


@receiver(pre_delete, sender=AttachmentArchive)
def remove_attachments(sender, **kwargs):
    instance = kwargs.get('instance')
    instance.remove_attachments()
    instance.remove_source_images()
    instance.remove_cache_images()
