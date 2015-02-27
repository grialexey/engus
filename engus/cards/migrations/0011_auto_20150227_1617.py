# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0010_auto_20150227_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='back_highlighted_text',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='front_highlighted_text',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
