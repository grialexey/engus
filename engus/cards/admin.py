import tempfile
from django.core.files import File
from django.db import models
from django.forms import Textarea
from django.contrib import admin
from django.template.defaultfilters import slugify
from pytils.translit import translify
from .models import Card, Deck
from .google_tts import audio_extract


def get_google_tts_audio(modeladmin, request, queryset):
    for card in queryset:
        with tempfile.NamedTemporaryFile() as temp:
            response = audio_extract(card.back)
            temp.write(response.read())
            temp.flush()
            translified = translify(card.back)
            file_name = slugify(translified)
            card.back_audio.save('%s.mp3' % file_name, File(temp))


class CardAdmin(admin.ModelAdmin):
    list_display = ('front', 'back', 'back_audio', 'learner', 'deck', 'weight', 'created', )
    ordering = ['-created', ]
    raw_id_fields = ('deck', 'learner')
    actions = [get_google_tts_audio, ]
    fieldsets = (
        ('Front', {
            'fields': ('front', 'front_image', 'front_audio', 'front_comment')
        }),
        ('Back', {
            'fields': ('back', 'back_image', 'back_audio', 'back_comment')
        }),
        ('Advanced options', {
            'fields': ('weight', 'deck', )
        }),
        ('Learner', {
            'fields': ('learner', 'level', 'next_repeat', )
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80, })},
    }


class CardInline(admin.TabularInline):
    model = Card
    raw_id_fields = ('learner', )
    fields = ('front', 'front_image', 'back', 'weight', 'learner', )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 50, })},
    }

    def get_queryset(self, request):
        qs = super(CardInline, self).get_queryset(request)
        return qs.exclude(deck__user__isnull=True, learner__isnull=False)


class DeckAdmin(admin.ModelAdmin):
    inlines = [CardInline, ]
    list_display = ('name', 'user', 'weight', 'created', )
    raw_id_fields = ('user', 'unit', )


admin.site.register(Card, CardAdmin)
admin.site.register(Deck, DeckAdmin)