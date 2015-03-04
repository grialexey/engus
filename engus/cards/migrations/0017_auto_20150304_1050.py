# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import engus.utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0016_auto_20150228_1824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deck',
            options={'ordering': ['weight', 'created'], 'verbose_name': 'Deck', 'verbose_name_plural': 'Decks'},
        ),
        migrations.RemoveField(
            model_name='deck',
            name='unit',
        ),
        migrations.DeleteModel(
            name='Unit',
        ),
        migrations.AddField(
            model_name='deck',
            name='unit_name',
            field=models.CharField(default='Basics', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='back_image',
            field=models.ImageField(upload_to=engus.utils.models.make_filepath, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='front_image',
            field=models.ImageField(upload_to=engus.utils.models.make_filepath, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deck',
            name='image',
            field=models.ImageField(upload_to=engus.utils.models.make_filepath, blank=True),
            preserve_default=True,
        ),
    ]
