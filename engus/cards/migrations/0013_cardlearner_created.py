# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0012_auto_20150228_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardlearner',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 28, 7, 47, 48, 325912, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
