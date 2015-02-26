# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_deck_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='author',
        ),
        migrations.RemoveField(
            model_name='deck',
            name='is_public',
        ),
        migrations.AlterField(
            model_name='card',
            name='deck',
            field=models.ForeignKey(default=1, to='cards.Deck'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='learner',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deck',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
