# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_auto_20150225_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='image',
            field=models.ImageField(default='', upload_to=b'card_image/%Y_%m_%d'),
            preserve_default=False,
        ),
    ]
