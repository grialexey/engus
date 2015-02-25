from django.db import models
from django.forms import Textarea
from django.contrib import admin
from .models import Card, UserCard, Deck


class CardAdmin(admin.ModelAdmin):
    list_display = ('front', 'back', 'author', 'created', )
    raw_id_fields = ('author', 'deck', )
    fieldsets = (
        ('Front', {
            'fields': ('front', 'front_image', 'front_audio', 'front_comment')
        }),
        ('Back', {
            'fields': ('back', 'back_image', 'back_audio', 'back_comment')
        }),
        ('Advanced options', {
            'fields': ('deck', 'author', )
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 80, })},
    }


class UserCardAdmin(admin.ModelAdmin):
    raw_id_fields = ('card', 'user', )


admin.site.register(Card, CardAdmin)
admin.site.register(UserCard, UserCardAdmin)
admin.site.register(Deck)