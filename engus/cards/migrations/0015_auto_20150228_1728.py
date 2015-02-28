# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0014_auto_20150228_1153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='subtitle',
        ),
        migrations.AlterField(
            model_name='deck',
            name='image',
            field=models.ImageField(upload_to=b'deck_image/%Y_%m_%d', blank=True),
            preserve_default=True,
        ),
    ]
