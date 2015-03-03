from django.http import JsonResponse, Http404
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.db.models import Count, Prefetch
from braces.views import LoginRequiredMixin
from .models import Card, Deck, CardLearner
from .forms import CardLearnerConfidenceForm


def home_view(request):
    if request.user.is_authenticated():
        decks = Deck.objects.filter(Q(user=request.user) | Q(user__isnull=True)).annotate(Count('card'))
        for deck in decks:
            deck.card_learners = CardLearner.objects.filter(card__deck=deck, learner=request.user)
            deck.learned_cards_count = deck.card_learners.learned().count()
        return render_to_response('cards/deck_list.html', {'deck_list': decks, },
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('home.html', context_instance=RequestContext(request))


class DeckDetailView(LoginRequiredMixin, DetailView):
    model = Deck

    def get_queryset(self):
        return Deck.objects.filter(Q(user=self.request.user) | Q(user__isnull=True)).select_related('card_set')


@login_required
def study_deck(request, pk):
    try:
        deck = Deck.objects.filter(Q(user=request.user) | Q(user__isnull=True)).get(pk=pk)
    except Deck.DoesNotExist:
        raise Http404
    response_data = {'deck': deck, }
    cards = Card.objects.filter(deck=deck)
    if cards.exists():
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
                    return redirect('/')
        else:
            card = cards[0]
            response_data['learned_cards_count'] = 0
        response_data['card'] = card
        response_data['study_mode'] = True
        return render_to_response('cards/deck_study.html', response_data, context_instance=RequestContext(request))
    else:
        return redirect('/')


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
