from django.http import JsonResponse, Http404
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db.models import Count, Prefetch
from braces.views import LoginRequiredMixin
from .models import Card, Deck, CardLearner
from .forms import CardLearnerConfidenceForm


def home_view(request):
    return render_to_response('home.html', context_instance=RequestContext(request))


class DeckListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Deck.objects.filter(Q(user=self.request.user) | Q(user__isnull=True)).annotate(Count('card'))

    def get_context_data(self, **kwargs):
        context = super(DeckListView, self).get_context_data(**kwargs)
        card_learners = CardLearner.objects.filter(learner=self.request.user).select_related('card')
        card_learners_decks_list = card_learners.values_list('card__deck', flat=True)
        learned_card_learners_decks_list = card_learners.learned().values_list('card__deck', flat=True)
        for deck in self.object_list:
            deck.card_learners_count = len([i for i in card_learners_decks_list if i == deck.pk])
            deck.learned_cards_count = len([i for i in learned_card_learners_decks_list if i == deck.pk])
        return context




class DeckDetailView(LoginRequiredMixin, DetailView):
    model = Deck

    def get_queryset(self):
        return Deck.objects.filter(Q(user=self.request.user) | Q(user__isnull=True)).select_related('card_set')

    def get_object(self):
        obj = super(DeckDetailView, self).get_object()
        if not obj.has_access_to_study(self.request.user):
            raise Http404
        return obj



@login_required
def study_deck(request, pk):
    try:
        deck = Deck.objects.filter(Q(user=request.user) | Q(user__isnull=True)).get(pk=pk)
    except Deck.DoesNotExist:
        raise Http404
    response_data = {'deck': deck, }
    cards = Card.objects.filter(deck=deck)
    if cards.exists() and deck.has_access_to_study(request.user):
        card_learners = CardLearner.objects.filter(card__in=cards, learner=request.user)
        if card_learners.exists():
            response_data['learned_cards_count'] = card_learners.learned().count()
            try:
                card_learner = card_learners.get_next_to_study()
                card = card_learner.card
                response_data['card_learner'] = card_learner
            except CardLearner.DoesNotExist:
                try:
                    card = cards.exclude(pk__in=card_learners.values_list('card', flat=True))[:1].get()
                except Card.DoesNotExist:
                    return redirect('cards:deck-list')
        else:
            card = cards[0]
            response_data['learned_cards_count'] = 0
        response_data['card'] = card
        response_data['study_mode'] = True
        return render_to_response('cards/deck_study.html', response_data, context_instance=RequestContext(request))
    else:
        return redirect('cards:deck-list')


@login_required
def confidence_change(request, pk):
    if request.method == 'POST':
        card = get_object_or_404(Card, pk=pk)
        card_learner, created = CardLearner.objects.get_or_create(card=card, learner=request.user)
        form = CardLearnerConfidenceForm(request.POST, instance=card_learner)
        if form.is_valid():
            form.update_level()
            form.save()
        return redirect(card.deck.get_study_url())
    else:
        raise Http404
