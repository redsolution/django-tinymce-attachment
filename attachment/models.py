# -*- coding: utf-8 -*-
import os
from django.db import models
from imagekit.models import ImageModel
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from attachment import settings
from .fields import ImagePreviewField


class AttachmentImage(ImageModel):
    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
        ordering = ('position',)

    class IKOptions:
        spec_module = settings.ATTACHMENT_IKSPECS
        cache_dir = settings.ATTACHMENT_CACHE_DIR
        cache_filename_format = "%(filename)s-%(specname)s.%(extension)s"
        image_field = 'image'

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    position = models.IntegerField(verbose_name=_('position'), default=1, blank=False)
    image = ImagePreviewField(verbose_name=_('image'), upload_to=settings.ATTACHMENT_UPLOAD_DIR)
    title = models.TextField(verbose_name=_('title'), blank=True, null=True)
    group = models.CharField(verbose_name=_('group'), max_length=200, blank=True, null=True)
    role = models.CharField(verbose_name=_('role'), max_length=200, blank=True, null=True)

    def __str__(self):
        if self.image:
            return os.path.basename(self.image.url)
        else:
            return u''


class AttachmentFile(models.Model):
    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    position = models.IntegerField(verbose_name=_('position'), default=1, blank=False)
    file = models.FileField(verbose_name=_('file'), upload_to=settings.ATTACHMENT_UPLOAD_DIR)
    title = models.TextField(verbose_name=_('title'), blank=True, null=True)

    def __str__(self):
        if self.file:
            return os.path.basename(self.file.url)
        else:
            return u''


class AttachmentArchive(models.Model):

    class Meta:
        verbose_name = u'Архив вложений'
        verbose_name_plural = u'Архивы вложений'

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    file_list = models.TextField(verbose_name=u'Список файлов', null=True, blank=True)
    uploaded_date = models.DateTimeField(verbose_name=u'Загружен', auto_now_add=True)
    unpacked = models.BooleanField(verbose_name=u'Распакован', default=False)

    zip_file = models.FileField(
        verbose_name=u'ZIP-архив',
        upload_to=settings.ATTACHMENT_UPLOAD_DIR,
        help_text=u'Внимание: загрузка и распаковка архива может занять длительное время'
    )
    use_filenames_as_titles = models.BooleanField(
        verbose_name=u'Использовать имена файлов в качестве заголовков',
        default=False
    )

    def __str__(self):
        title = 'Null' if not self.content_object else self.content_object._meta.verbose_name.title()
        return u'{model} - {object}'.format(
            model=title,
            object=self.content_object
        )

    def files_count(self):
        if self.file_list:
            return len(self.file_list.splitlines())
        return 0

    def get_attachments(self):
        if self.file_list:
            return AttachmentImage.objects.filter(
                content_type=self.content_type,
                object_id=self.object_id,
                image__in=self.file_list.splitlines()
            )
        return AttachmentImage.objects.none()

    def get_attachment_list(self):
        return list(self.get_attachments())

    def remove_attachments(self):
        self.get_attachments().delete()

    def remove_source_images(self):
        if self.file_list:
            for attachment_file in self.file_list.splitlines():
                path_to_file = os.path.join(settings.MEDIA_ROOT, attachment_file)
                try:
                    os.remove(path_to_file)
                except OSError:
                    pass

    def _get_filename(self, name_ext):
        if '.' in os.path.basename(name_ext):
            return os.path.basename(name_ext).rpartition('.')[0]
        else:
            return os.path.basename(name_ext)

    def remove_cache_images(self):
        if self.file_list:
            path_to_cache_dir = os.path.join(settings.MEDIA_ROOT, settings.ATTACHMENT_CACHE_DIR, settings.ATTACHMENT_UPLOAD_DIR)
            cache_list = os.listdir(path_to_cache_dir)
            for attachment_file in self.file_list.splitlines():
                name_without_ext = self._get_filename(attachment_file)
                cache_files = []
                for image in cache_list:
                    try:
                        if name_without_ext in image:
                            os.path.join(path_to_cache_dir, image)
                    # если название файла на кириллице
                    except UnicodeDecodeError:
                        pass

                for path_to_file in cache_files:
                    try:
                        os.remove(path_to_file)
                    except OSError:
                        pass
