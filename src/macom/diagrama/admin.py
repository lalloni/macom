# -*- coding: utf-8 -*-

from django.contrib import admin
from macom.diagrama import models
from django.utils.translation import ugettext_lazy as _
import settings

media = settings.MEDIA_URL

class InlineInterface(admin.StackedInline):
    model = models.Interface
    #fields = ['exposer', 'name', 'goal', 'technology', 'direction_inbound', 'direction_outbound']
    fieldsets = (
        (None, {
            'fields': ('exposer', 'name')
        }),
        ('Detail', {
            'classes': ('collapse',),
            'fields': ('goal','technology','direction_inbound', 'direction_outbound')
        }),
    )

    list_display = ['exposer', 'name', 'goal', 'technology']
    verbose_name = _('Interface')
    verbose_name_plural = _('Interfaces')
    extra = 0

class InlineDependency(admin.StackedInline):
    model = models.Dependency
    extra = 0
    #fields = ['exposer','interface','goal','technology','direction_inbound', 'direction_outbound','referents', 'documentation']
    fieldsets = (
        (None, {
            'fields': ('exposer','interface')
        }),
        ('Detail', {
            'classes': ('collapse',),
            'fields': ('goal','technology','direction_inbound', 'direction_outbound','referents', 'documentation')
        }),
    )

    list_display = ['interface', 'goal', 'referents', 'documentation']
    search_fields = ['exposer__name', 'name']
    ordering = ['exposer__system__name']

class ModuleAdmin(admin.ModelAdmin):
	#fields = ['system', 'name', 'goal', 'referents', 'documentation', 'external', 'criticity', 'consumed' ]
    fieldsets = (
        ('Identification', {
            'fields': ('system', 'name',  'external')
        }),
        ('Detail', {
            'classes': ('collapse',),
            'fields': ('goal','criticity','referents', 'documentation')
        }),
    )
    #filter_horizontal = ['consumed']
    list_display = ['system', 'name', 'goal', 'external']
    list_display_links = ['name']
    
    search_fields = ['system__name','name', 'goal']
    inlines = [InlineInterface, InlineDependency]

class SystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'referents', 'documentation', 'external']
    search_fields = ['name', 'description']
    
class InterfaceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identification', {
            'fields': ('exposer', 'name')
        }),
        ('Direction', {
            'classes': ('wide',),
            'fields': ('direction_inbound', 'direction_outbound')
        }),
        ('Detail', {
            'classes': ('collapse',),
            'fields': ('goal','technology','referents', 'documentation')
        }),
    )
    list_display = ['exposer', 'name', 'goal', 'referents', 'documentation']
    list_display_links = ['name']
    ordering = ['exposer__system__name']
    search_fields = ['exposer__name', 'name']

class DependencyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identification', {
            'fields': ('exposer','interface')
        }),
        ('Direction', {
            'classes': ('wide',),
            'fields': ('direction_inbound', 'direction_outbound')
        }),
        ('Detail', {
            'classes': ('collapse',),
            'fields': ('goal','technology','loadestimate', 'referents', 'documentation')
        }),
    )
    list_display = ['exposer', 'interface', 'goal', 'referents', 'documentation']
    list_display_links = ['exposer']
    ordering = ['exposer__system__name']
    search_fields = ['exposer__name']

admin.site.register(models.Dependency, DependencyAdmin)
admin.site.register(models.Interface, InterfaceAdmin)
admin.site.register(models.Module, ModuleAdmin)
admin.site.register(models.System, SystemAdmin)
