from django.conf.urls import patterns, url
from .views import study_deck, confidence_change


urlpatterns = patterns('',
    url(r'^decks/(?P<pk>\d+)/study/$', study_deck, name='deck-study'),
    url(r'^cards/(?P<pk>\d+)/confidence-change/$', confidence_change, name='card-confidence-change'),
)