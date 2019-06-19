# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import attachment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attachment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachmentfile',
            name='file',
            field=models.FileField(upload_to=b'upload/attachment/source', max_length=255, verbose_name='file'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attachmentimage',
            name='image',
            field=attachment.fields.ImagePreviewField(upload_to=b'upload/attachment/source', max_length=255, verbose_name='image'),
            preserve_default=True,
        ),
    ]
