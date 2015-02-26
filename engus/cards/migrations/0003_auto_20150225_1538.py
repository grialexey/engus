# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cards', '0002_auto_20150225_1247'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usercard',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='usercard',
            name='card',
        ),
        migrations.RemoveField(
            model_name='usercard',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserCard',
        ),
        migrations.AddField(
            model_name='card',
            name='learner',
            field=models.ForeignKey(related_name='card_set_to_study', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='level',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='next_repeat',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deck',
            name='is_public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deck',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='author',
            field=models.ForeignKey(related_name='card_set', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
