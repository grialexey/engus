# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0018_auto_20150304_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='unit_color',
            field=models.CharField(max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
