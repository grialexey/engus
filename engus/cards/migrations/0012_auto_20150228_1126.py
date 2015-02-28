# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cards', '0011_auto_20150227_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardLearner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.PositiveIntegerField(default=0)),
                ('next_repeat', models.DateTimeField(null=True, blank=True)),
                ('card', models.ForeignKey(to='cards.Card')),
                ('learner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='cardlearner',
            unique_together=set([('card', 'learner')]),
        ),
        migrations.RemoveField(
            model_name='card',
            name='learner',
        ),
        migrations.RemoveField(
            model_name='card',
            name='level',
        ),
        migrations.RemoveField(
            model_name='card',
            name='next_repeat',
        ),
    ]
