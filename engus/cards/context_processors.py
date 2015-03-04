from .models import CardLearner


def cards_learned_count(request):
    cards_count = 0
    if request.user.is_authenticated():
        cards_count = CardLearner.objects.filter(learner=request.user).learned().count()
    return {
        'cards_learned_count': cards_count,
    }