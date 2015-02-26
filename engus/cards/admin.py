from django.db import models
from django.forms import Textarea
from django.contrib import admin
from .models import Card, Deck


class CardAdmin(admin.ModelAdmin):
    list_display = ('front', 'back', 'created', )
    raw_id_fields = ('deck', 'learner')
    fieldsets = (
        ('Front', {
            'fields': ('front', 'front_image', 'front_audio', 'front_comment')
        }),
        ('Back', {
            'fields': ('back', 'back_image', 'back_audio', 'back_comment')
        }),
        ('Advanced options', {
            'fields': ('deck', )
        }),
        ('Learner', {
            'fields': ('learner', 'level', 'next_repeat', )
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80, })},
    }


class DeckAdmin(admin.ModelAdmin):
    pass


admin.site.register(Card, CardAdmin)
admin.site.register(Deck, DeckAdmin)