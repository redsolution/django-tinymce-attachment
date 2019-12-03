# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import attachment.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachmentFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('file', models.FileField(upload_to=b'upload/attachment/source', verbose_name='file')),
                ('position', models.IntegerField(default=1, verbose_name='position')),
                ('title', models.TextField(null=True, verbose_name='title', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'file',
                'verbose_name_plural': 'files',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttachmentImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('image', attachment.fields.ImagePreviewField(upload_to=b'upload/attachment/source', verbose_name='image')),
                ('position', models.IntegerField(default=1, verbose_name='position')),
                ('title', models.TextField(null=True, verbose_name='title', blank=True)),
                ('group', models.CharField(max_length=200, null=True, verbose_name='group', blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
            },
            bases=(models.Model,),
        ),
    ]
