# -*- coding: utf-8 -*-

from polls.models import Poll, Choice
from django.contrib import admin

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'pub_date']
    list_filter = ['question']
    search_fields = ['question']
    inlines = [ChoiceInline]
    fieldsets = [
        (None, {'fields': ['question']}),
        ('Info de Fechas', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    
admin.site.register(Poll, PollAdmin)