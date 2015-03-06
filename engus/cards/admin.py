import tempfile
from django.core.files import File
from django.db import models
from django.forms import Textarea, TextInput
from django.contrib import admin
from django.template.defaultfilters import slugify, striptags
from pytils.translit import translify
from .models import Card, Deck, CardLearner
from .google_tts import audio_extract


def get_google_tts_audio(modeladmin, request, queryset):
    for card in queryset:
        with tempfile.NamedTemporaryFile() as temp:
            text = striptags(card.back)
            response = audio_extract(text)
            temp.write(response.read())
            temp.flush()
            translified = translify(text)
            file_name = slugify(translified)[:50]
            card.back_audio.save('%s.mp3' % file_name, File(temp))


class CardAdmin(admin.ModelAdmin):
    list_display = ('front', 'back', 'back_audio', 'deck', 'weight', 'created', )
    ordering = ['-created', ]
    raw_id_fields = ('deck', )
    actions = [get_google_tts_audio, ]
    fieldsets = (
        ('Back', {
            'fields': ('back', 'back_highlighted_text', 'back_image', 'back_audio', 'back_comment')
        }),
        ('Front', {
            'fields': ('front', 'front_highlighted_text', 'front_image', 'front_audio', 'front_comment')
        }),
        ('Advanced options', {
            'fields': ('weight', 'deck', )
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80, })},
    }


class CardInline(admin.TabularInline):
    model = Card
    fields = ('back', 'back_highlighted_text', 'front', 'front_highlighted_text', 'front_image', 'weight', )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 50, })},
        models.CharField: {'widget': TextInput(attrs={'size': 30, })},
    }
    extra = 5


class DeckAdmin(admin.ModelAdmin):
    inlines = [CardInline, ]
    list_display = ('name', 'user', 'previous_decks_cards_count', 'weight', 'created', )
    list_editable = ('weight', )
    raw_id_fields = ('user', )

    def previous_decks_cards_count(self, obj):
        cards_count = 0
        if obj.user is None:
            decks = Deck.objects.filter(weight__lt=obj.weight, user__isnull=True)
            cards_count = Card.objects.filter(deck__in=decks).count()
        return cards_count

    readonly_fields = ('previous_decks_cards_count', )


class CardLearnerAdmin(admin.ModelAdmin):
    list_display = ('card', 'learner', 'level', 'next_repeat', 'created', )
    raw_id_fields = ('card', 'learner', )
    ordering = ('-created', )


admin.site.register(Card, CardAdmin)
admin.site.register(Deck, DeckAdmin)
admin.site.register(CardLearner, CardLearnerAdmin)