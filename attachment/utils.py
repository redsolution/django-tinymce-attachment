# -*- coding: utf-8 -*-
import re
from random import randint
from attachment.settings import ATTACHMENT_UPLOAD_DIR
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_text
from attachment.models import AttachmentImage
from os.path import join, basename, isfile
from shutil import rmtree
from unidecode import unidecode
from zipfile import ZipFile, BadZipfile
import os


class ZipExtractor(object):

    _has_error = False

    def __init__(self, attachment_archive_instance):
        self.attachment_archive_instance = attachment_archive_instance
        self.content_type = attachment_archive_instance.content_type
        self.object_id = attachment_archive_instance.object_id
        self.path_to_zip_file = attachment_archive_instance.zip_file.path
        try:
            self.zip_file = ZipFile(self.path_to_zip_file, 'r')
            self.use_filenames_as_titles = attachment_archive_instance.use_filenames_as_titles
            self.upload_dir = join(settings.MEDIA_ROOT, ATTACHMENT_UPLOAD_DIR)
            self.extract_dir = join(self.upload_dir, 'tmp')
            self.groups = []
            self.file_list = ''
        except BadZipfile:
            self._has_error = True
            self._finalize()

    def _update_file_list(self):
        AttachmentArchive = self.attachment_archive_instance.__class__
        AttachmentArchive.objects.filter(id=self.attachment_archive_instance.id).update(
            file_list=self.file_list,
            unpacked=True
        )

    def _finalize(self):
        if not self._has_error:
            self.zip_file.close()
            rmtree(self.extract_dir)
            self._update_file_list()
        os.remove(self.path_to_zip_file)

    def _is_root_file(self, path):
        return not os.sep in path

    def _is_first_level_dir(self, path):
        return path.endswith(os.sep) and path.count(os.sep) == 1

    def _get_image_title(self, path):
        if '.' in basename(path):
            return basename(path).rpartition('.')[0] if self.use_filenames_as_titles else ''
        else:
            return basename(path) if self.use_filenames_as_titles else ''

    def _get_obfuscated_name(self, name):
        return '%s-%04x' % (name, randint(0, 0x10000))

    def _make_filename(self, path):
        if '.' in basename(path):
            ext = ''.join(basename(path).rpartition('.')[-2:])
            filename = basename(path).rpartition('.')[0]
        else:
            ext = ''
            filename = basename(path)
        filename = re.sub(r'[_.,:;@#$%^&?*|()\[\]]', '-', filename)
        return self._get_obfuscated_name(slugify(unidecode(smart_text(filename)))) + ext

    def _get_path_to_file(self, path):
        return join(self.upload_dir, path)

    def _normalize_filename(self, filename, group=None):
        if group is None:
            current_path = join(self.extract_dir, basename(filename))
        else:
            current_path = join(self.extract_dir, group, basename(filename))
        new_filename = self._make_filename(filename)
        new_path = join(self.upload_dir, new_filename)
        os.rename(current_path, new_path)
        return join(ATTACHMENT_UPLOAD_DIR, new_filename)

    def _is_image_file(self, path_to_file):
        return isfile(path_to_file) and \
               (path_to_file.endswith('.jpg') or path_to_file.endswith('.png') or path_to_file.endswith('.gif') or path_to_file.endswith('.jpeg'))

    def _create_attachment_image(self, filename, group='', position=1):
        title = self._get_image_title(filename)
        path_to_image = self._normalize_filename(filename, group)
        AttachmentImage.objects.create(
            content_type=self.content_type,
            object_id=self.object_id,
            image=path_to_image,
            title=title,
            position=position,
            group=group
        )
        self.file_list += '{attachment_file}\n'.format(attachment_file=path_to_image)

    def _namelist(self):
        result = []
        for name in self.zip_file.namelist():
            try:
                if not self._check_unicode(name):
                    name = name.decode('cp866')
            except UnicodeDecodeError:
                pass
            result.append(name)
        return result

    def _fix_win_encoding(self):
        for root, dirs, files in os.walk(self.extract_dir):
            for d in dirs:
                path = os.path.join(root, d)
                try:
                    if not self._check_unicode(path):
                        new_path = path.decode('cp866')
                        os.rename(path, new_path)
                except UnicodeDecodeError:
                    pass
            for f in files:
                path = os.path.join(root, f)
                try:
                    if not self._check_unicode(path):
                        new_path = path.decode('cp866')
                        os.rename(path, new_path)
                except UnicodeDecodeError:
                    pass

    def _check_unicode(self, string):
        if type(string) == unicode:
            return True
        try:
            return string.decode('utf-8').encode('utf-8') == string
        except UnicodeDecodeError as UnicodeEncodeError:
            return False

    def make_attachments(self):
        if not self._has_error:
            self.zip_file.extractall(path=self.extract_dir)
            self._fix_win_encoding()
            position = 0
            for file in sorted(self._namelist()):
                if self._is_root_file(file):
                    path_to_file = join(self.extract_dir, file)
                    if self._is_image_file(path_to_file):
                        position += 1
                        self._create_attachment_image(file, position=position)
                    else:
                        os.remove(path_to_file)
                else:
                    if self._is_first_level_dir(file):
                        self.groups.append(file)
            for group in self.groups:
                path_to_group_dir = join(self.extract_dir, group)
                position = 0
                for file in sorted(os.listdir(path_to_group_dir)):
                    path_to_file = join(path_to_group_dir, file)
                    if self._is_image_file(path_to_file):
                        position += 1
                        self._create_attachment_image(file, group=group[:-1], position=position)
                rmtree(path_to_group_dir)
            self._finalize()
