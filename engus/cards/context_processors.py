from .models import CardLearner


def user_level(request):
    cards_count = 0
    if request.user.is_authenticated():
        cards_count = CardLearner.objects.filter(learner=request.user).learned().count()
    return {
        'user_level': cards_count,
    }