from django.conf.urls import patterns, url
from .views import study_deck


urlpatterns = patterns('',
    url(r'^decks/(?P<pk>\d+)/study/$', study_deck, name='deck-study'),
)