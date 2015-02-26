from django.http import JsonResponse, Http404
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Card, Deck
from .forms import CardConfidenceForm


def home_view(request):
    if request.user.is_authenticated():
        decks = Deck.objects.filter(Q(user=request.user) | Q(user__isnull=True))
        for deck in decks:
            user_cards_in_deck = Card.objects.filter(deck=deck, learner=request.user)
            if user_cards_in_deck.exists():
                deck.all_user_cards_count = user_cards_in_deck.count()
                deck.learned_user_cards_count = user_cards_in_deck.learned().count()
        return render_to_response('cards/deck_list.html', {'deck_list': decks, },
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('home.html', context_instance=RequestContext(request))


@login_required
def study_deck(request, pk):
    if request.method == 'POST':
        try:
            card_to_update = Card.objects.get(pk=request.POST.get('card'), learner=request.user)
            form = CardConfidenceForm(request.POST, instance=card_to_update)
            if form.is_valid():
                form.update_level()
                form.save()
        except Card.DoesNotExist:
            pass
    deck = get_object_or_404(Deck, pk=pk)
    cards = Card.objects.filter(deck=deck, learner=request.user)
    if not cards.exists():
        deck.copy_public_cards_to_user(request.user)
        cards = Card.objects.filter(deck=deck, learner=request.user)
    if cards.exists():
        try:
            card = cards.get_card_to_study()
        except Card.DoesNotExist:
            return redirect('/')
        all_cards_in_deck = Card.objects.filter(learner=request.user, deck=deck)
        learned_cards_in_deck = all_cards_in_deck.learned()
        response_data = {
            'card': card,
            'deck': deck,
            'learned_cards_in_deck': learned_cards_in_deck.count(),
            'all_cards_in_deck': all_cards_in_deck.count(),
        }
        return render_to_response('cards/deck_study.html', response_data,
                                  context_instance=RequestContext(request))
    else:
        raise Http404