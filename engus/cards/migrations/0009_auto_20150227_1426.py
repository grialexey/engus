# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0008_auto_20150226_2101'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['-weight', '-created'], 'verbose_name': 'Card', 'verbose_name_plural': 'Cards'},
        ),
        migrations.AddField(
            model_name='card',
            name='weight',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
