from django.conf.urls import patterns, url
from .views import study_deck, confidence_change, DeckDetailView


urlpatterns = patterns('',
    url(r'^decks/(?P<pk>\d+)/study/$', study_deck, name='deck-study'),
    url(r'^decks/(?P<pk>\d+)/$', DeckDetailView.as_view(), name='deck-detail'),
    url(r'^cards/(?P<pk>\d+)/confidence-change/$', confidence_change, name='card-confidence-change'),
)