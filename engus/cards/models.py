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
    user = models.ForeignKey(User, null=True, blank=True)
    image = models.ImageField(upload_to='deck_image/%Y_%m_%d', blank=True)
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


class Card(models.Model):
    front = models.TextField(blank=True)
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
    weight = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
        ordering = ['weight', 'created', 'pk', ]

    def __unicode__(self):
        return u'#%d. %s – %s' % (self.pk, self.front, self.back)


class CardLearnerQuerySet(models.QuerySet):

    def to_repeat(self):
        return self.filter(next_repeat__lt=timezone.now()).order_by('-next_repeat')

    def not_studied(self):
        return self.filter(next_repeat__isnull=True)

    def learned(self):
        return self.filter(next_repeat__gt=timezone.now())

    def get_next_to_study(self):
        try:
            return self.to_repeat()[:1].get()
        except Card.DoesNotExist:
            return self.not_studied()[:1].get()


class CardLearnerManager(models.Manager):

    def get_queryset(self):
        return super(CardLearnerManager, self).get_queryset().select_related('card')


class CardLearner(models.Model):
    card = models.ForeignKey(Card)
    learner = models.ForeignKey(User)
    level = models.PositiveIntegerField(default=1)
    next_repeat = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    objects = CardLearnerManager().from_queryset(CardLearnerQuerySet)()

    class Meta:
        unique_together = ('card', 'learner', )

    def __unicode__(self):
        return u'%s. Learner: %s' % (self.card.back, self.learner.username)

    def save(self, *args, **kwargs):
        self.set_next_repeat()
        super(CardLearner, self).save(*args, **kwargs)

    def is_to_repeat(self):
        return self.next_repeat < timezone.now()

    def set_next_repeat(self):
        self.next_repeat = timezone.now() + datetime.timedelta(minutes=self.level ** 2)

    def update_level(self, confidence):
        if self.level < 5 and confidence < 5:
            self.level = confidence
        else:
            self.level *= 2
        self.set_next_repeat()