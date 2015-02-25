# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('front', models.TextField()),
                ('front_audio', models.FileField(upload_to=b'card_audio/%Y_%m_%d', blank=True)),
                ('front_image', models.ImageField(upload_to=b'card_image/%Y_%m_%d', blank=True)),
                ('front_comment', models.TextField()),
                ('back', models.TextField()),
                ('back_audio', models.FileField(upload_to=b'card_audio/%Y_%m_%d', blank=True)),
                ('back_image', models.ImageField(upload_to=b'card_image/%Y_%m_%d', blank=True)),
                ('back_comment', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Card',
                'verbose_name_plural': 'Cards',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Cards deck',
                'verbose_name_plural': 'Cards decks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.PositiveIntegerField(default=0)),
                ('next_repeat', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0421\u043e\u0437\u0434\u0430\u043d\u0430')),
                ('card', models.ForeignKey(to='cards.Card')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'User card',
                'verbose_name_plural': 'User cards',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='usercard',
            unique_together=set([('card', 'user')]),
        ),
        migrations.AddField(
            model_name='card',
            name='deck',
            field=models.ForeignKey(blank=True, to='cards.Deck', null=True),
            preserve_default=True,
        ),
    ]
