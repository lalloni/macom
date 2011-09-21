# -*- coding: utf-8 -*-

from django.contrib import admin
from macom.diagrama import models
from django.utils.translation import ugettext_lazy as _

class InlineInterface(admin.TabularInline):
    model = models.Interface
    
    fieldsets = (
        (None, {
            'fields': ('exposer', 'name')
        }),
        ('Referencias', {
            'classes': ('wide',),
            'fields': ('goal', 'technology')
        }),
        ('Direction', {
            'classes': ('wide',),
            'fields': ('direction_inbound', 'direction_outbound')
        }),
    )

#fields = ['exposer', 'name', 'goal', 'technology', 'direction_inbound', 'direction_outbound']
    list_display = ['exposer', 'name', 'goal', 'technology']
    verbose_name = _('Interface')
    verbose_name_plural = _('Interfaces')
    extra = 0
            
class ModuleAdmin(admin.ModelAdmin):
#    fields = ['system', 'name', 'goal', 'referents', 'documentation', 'external', 'criticity', 'consumed' ]

    fieldsets = (
        (None, {
            'fields': ('system', 'name', 'goal', 'external')
        }),
        ('Reference', {
            'classes': ('wide',),
            'fields': ('referents', 'documentation')
        }),
        ('Dependencies', {
            'classes': ('wide',),
            'fields': ('criticity','consumed')    
        }),
    )

    filter_horizontal = ['consumed']
    list_display = ['system', 'name', 'goal', 'external']
    list_display_links = ['name']
    search_fields = ['system__name','name', 'goal']
    inlines = [InlineInterface]

class SystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'referents', 'documentation', 'external']
    search_fields = ['name', 'description']
    
class InterfaceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('exposer', 'name', 'goal')
        }),
        ('Reference', {
            'classes': ('wide',),
            'fields': ('referents', 'documentation')
        }),
    )

    list_display = ['exposer', 'name', 'goal', 'referents', 'documentation']
    list_display_links = ['name']
    ordering = ['exposer']
    search_fields = ['exposer__name', 'name']

admin.site.register(models.Interface, InterfaceAdmin)
admin.site.register(models.Module, ModuleAdmin)
admin.site.register(models.System, SystemAdmin)