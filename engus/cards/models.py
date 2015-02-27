# -*- coding: utf-8 -*-
import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Unit(models.Model):
    name = models.CharField(max_length=255)
    weight = models.BooleanField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        ordering = ['-weight', '-created', ]

    def __unicode__(self):
        return self.name


class Deck(models.Model):
    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    image = models.ImageField(upload_to='card_image/%Y_%m_%d')
    unit = models.ForeignKey(Unit, null=True, blank=True)
    weight = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Deck'
        verbose_name_plural = 'Decks'
        ordering = ['-unit__weight', '-weight', '-created', ]

    def __unicode__(self):
        if self.user:
            return '%s. User: %s' % (self.name, self.user.username)
        return self.name

    def get_study_url(self):
        return reverse('cards:deck-study', kwargs={'pk': self.pk, })

    def copy_public_cards_to_user(self, user):
        for card in self.card_set.public():
            card.make_copy(user)


class CardQuerySet(models.QuerySet):

    def to_repeat(self):
        return self.filter(next_repeat__lt=timezone.now()).order_by('next_repeat')

    def not_studied(self):
        return self.filter(next_repeat__isnull=True)

    def learned(self):
        return self.filter(next_repeat__gt=timezone.now())

    def public(self):
        return self.filter(learner__isnull=True)

    def get_card_to_study(self):
        try:
            return self.to_repeat()[:1].get()
        except Card.DoesNotExist:
            return self.not_studied()[:1].get()


class CardManager(models.Manager):

    def get_queryset(self):
        return super(CardManager, self).get_queryset().select_related('card')


class Card(models.Model):
    front = models.TextField()
    front_highlighted_text = models.CharField(max_length=255, blank=True)
    front_audio = models.FileField(blank=True, upload_to='card_audio/%Y_%m_%d')
    front_image = models.ImageField(blank=True, upload_to='card_image/%Y_%m_%d')
    front_comment = models.TextField(blank=True)
    back = models.TextField()
    back_highlighted_text = models.CharField(max_length=255, blank=True)
    back_audio = models.FileField(blank=True, upload_to='card_audio/%Y_%m_%d')
    back_image = models.ImageField(blank=True, upload_to='card_image/%Y_%m_%d')
    back_comment = models.TextField(blank=True)
    deck = models.ForeignKey(Deck)
    learner = models.ForeignKey(User, null=True, blank=True)
    level = models.PositiveIntegerField(default=0)
    next_repeat = models.DateTimeField(null=True, blank=True)
    weight = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    objects = CardManager().from_queryset(CardQuerySet)()

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
        ordering = ['weight', 'created', 'pk', ]

    def __unicode__(self):
        return u'#%d. %s – %s' % (self.pk, self.front, self.back)

    def make_copy(self, learner):
        new_card = self
        new_card.pk = None
        new_card.next_repeat = None
        new_card.level = 0
        new_card.learner = learner
        new_card.save()
        return new_card

    def is_to_repeat(self):
        return self.next_repeat < timezone.now()

    def set_next_repeat(self):
        self.next_repeat = timezone.now() + datetime.timedelta(minutes=self.level ** 2)

    def update_level(self, confidence):
        if self.level >= 5 and confidence >= 5:
            self.level *= 2
        else:
            self.level = confidence
        self.set_next_repeat()
