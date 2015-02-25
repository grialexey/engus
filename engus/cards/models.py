# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone


class Deck(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Cards deck'
        verbose_name_plural = 'Cards decks'


class Card(models.Model):
    front = models.TextField()
    front_audio = models.FileField(blank=True, upload_to='card_audio/%Y_%m_%d')
    front_image = models.ImageField(blank=True, upload_to='card_image/%Y_%m_%d')
    front_comment = models.TextField(blank=True)
    back = models.TextField()
    back_audio = models.FileField(blank=True, upload_to='card_audio/%Y_%m_%d')
    back_image = models.ImageField(blank=True, upload_to='card_image/%Y_%m_%d')
    back_comment = models.TextField(blank=True)
    deck = models.ForeignKey(Deck, null=True, blank=True)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
        ordering = ['-created', ]

    def __unicode__(self):
        return u'#%d. %s – %s' % (self.pk, self.front, self.back)


class UserCardQuerySet(models.QuerySet):

    def to_repeat(self):
        return self.filter(next_repeat__lt=timezone.now())

    def learned(self):
        return self.filter(next_repeat__gt=timezone.now())


class UserCardManager(models.Manager):

    def get_queryset(self):
        return super(UserCardManager, self).get_queryset().select_related('card')


class UserCard(models.Model):
    card = models.ForeignKey(Card)
    user = models.ForeignKey(User)
    level = models.PositiveIntegerField(default=0)
    next_repeat = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Создана')

    objects = UserCardManager().from_queryset(UserCardQuerySet)()

    class Meta:
        unique_together = ('card', 'user')
        verbose_name = 'User card'
        verbose_name_plural = 'User cards'
        ordering = ['-created', ]

    def is_to_repeat(self):
        return self.next_repeat < timezone.now()

    def set_next_repeat(self):
        self.next_repeat = timezone.now() + datetime.timedelta(minutes=1) * (self.level ** 3.14)

    def good(self):
        if self.is_to_repeat():
            self.level += 1
            self.set_next_repeat()

    def bad(self):
        self.level = 0
        self.set_next_repeat()

