# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0019_deck_unit_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='unit_color',
        ),
        migrations.RemoveField(
            model_name='deck',
            name='unit_name',
        ),
    ]
