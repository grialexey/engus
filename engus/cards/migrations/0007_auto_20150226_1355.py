# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_auto_20150226_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('weight', models.BooleanField(default=0)),
            ],
            options={
                'ordering': ['-weight'],
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='deck',
            options={'ordering': ['-unit__weight', '-weight'], 'verbose_name': 'Deck', 'verbose_name_plural': 'Decks'},
        ),
        migrations.AddField(
            model_name='deck',
            name='unit',
            field=models.ForeignKey(blank=True, to='cards.Unit', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deck',
            name='weight',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
