# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0013_cardlearner_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardlearner',
            name='level',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cardlearner',
            name='next_repeat',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 28, 7, 53, 50, 551613, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
