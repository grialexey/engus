# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0009_auto_20150227_1426'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['weight', 'created', 'pk'], 'verbose_name': 'Card', 'verbose_name_plural': 'Cards'},
        ),
        migrations.AddField(
            model_name='deck',
            name='subtitle',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
