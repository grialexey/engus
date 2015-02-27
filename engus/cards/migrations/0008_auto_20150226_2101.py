# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_auto_20150226_1355'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deck',
            options={'ordering': ['-unit__weight', '-weight', '-created'], 'verbose_name': 'Deck', 'verbose_name_plural': 'Decks'},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'ordering': ['-weight', '-created'], 'verbose_name': 'Unit', 'verbose_name_plural': 'Units'},
        ),
        migrations.AddField(
            model_name='deck',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 26, 17, 1, 48, 495676, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unit',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 26, 17, 1, 55, 66919, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
