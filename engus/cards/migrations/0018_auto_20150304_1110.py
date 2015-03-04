# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0017_auto_20150304_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='weight',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
