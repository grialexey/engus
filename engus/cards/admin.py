import tempfile
from django.core.files import File
from django.db import models
from django.forms import Textarea
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
        ('Front', {
            'fields': ('front', 'front_highlighted_text', 'front_image', 'front_audio', 'front_comment')
        }),
        ('Back', {
            'fields': ('back', 'back_highlighted_text', 'back_image', 'back_audio', 'back_comment')
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
    fields = ('front', 'front_highlighted_text', 'front_image', 'back', 'back_highlighted_text',  'weight', )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 50, })},
    }


class DeckAdmin(admin.ModelAdmin):
    inlines = [CardInline, ]
    list_display = ('name', 'user', 'weight', 'created', )
    raw_id_fields = ('user', 'unit', )


class CardLearnerAdmin(admin.ModelAdmin):
    list_display = ('card', 'learner', 'level', 'next_repeat', 'created', )
    raw_id_fields = ('learner', )
    ordering = ('-created', )


admin.site.register(Card, CardAdmin)
admin.site.register(Deck, DeckAdmin)
admin.site.register(CardLearner, CardLearnerAdmin)