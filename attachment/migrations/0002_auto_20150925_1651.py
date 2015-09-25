# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachmentfile',
            name='position',
            field=models.IntegerField(default=1, verbose_name='position'),
        ),
        migrations.AlterField(
            model_name='attachmentfile',
            name='title',
            field=models.TextField(null=True, verbose_name='title', blank=True),
        ),
        migrations.AlterField(
            model_name='attachmentimage',
            name='title',
            field=models.TextField(null=True, verbose_name='title', blank=True),
        ),
    ]
