# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0015_auto_20150228_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='front',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
