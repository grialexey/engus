# -*- coding: utf-8 -*-
import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from engus.utils.models import make_filepath


class Deck(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, blank=True)
    image = models.ImageField(blank=True, upload_to=make_filepath)
    weight = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Deck'
        verbose_name_plural = 'Decks'
        ordering = ['weight', 'created', ]

    def __unicode__(self):
        if self.user:
            return '%s. User: %s' % (self.name, self.user.username)
        return self.name

    def get_study_url(self):
        return reverse('cards:deck-study', kwargs={'pk': self.pk, })

    def get_absolute_url(self):
        return reverse('cards:deck-detail', kwargs={'pk': self.pk, })

    def has_access_to_study(self, user):
        return user.cardlearner_set.learned().count() >= self.weight


class Card(models.Model):
    front = models.TextField(blank=True)
    front_highlighted_text = models.CharField(max_length=255, blank=True)
    front_audio = models.FileField(blank=True, upload_to='card_audio/%Y_%m_%d')
    front_image = models.ImageField(blank=True, upload_to=make_filepath)
    front_comment = models.TextField(blank=True)
    back = models.TextField()
    back_highlighted_text = models.CharField(max_length=255, blank=True)
    back_audio = models.FileField(blank=True, upload_to='card_audio/%Y_%m_%d')
    back_image = models.ImageField(blank=True, upload_to=make_filepath)
    back_comment = models.TextField(blank=True)
    deck = models.ForeignKey(Deck)
    weight = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
        ordering = ['weight', 'created', 'pk', ]

    def save(self, *args, **kwargs):
        if self.pk is None:
            previous_card = Card.objects.filter(deck=self.deck).last()
            if previous_card is not None:
                self.weight = previous_card.weight + 100
        super(Card, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s – %s. Deck: %s' % (self.front, self.back, self.deck)


class CardLearnerQuerySet(models.QuerySet):

    def to_repeat(self):
        return self.filter(next_repeat__lt=timezone.now()).order_by('level', '-next_repeat')

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
        if self.level >= 5 and confidence >= 5:
            self.level *= 2
        else:
            self.level = confidence
        self.set_next_repeat()