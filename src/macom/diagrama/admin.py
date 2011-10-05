# -*- coding: utf-8 -*-

from django.contrib import admin
from macom.diagrama import models
from django.utils.translation import ugettext_lazy as _

class InlineInterface(admin.StackedInline):
    model = models.Interface
    extra = 0
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

class InlineDependency(admin.StackedInline):
    model = models.Dependency
    extra = 0
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
    search_fields = ['exposer__name', 'name','referents', 'documentation','technology']
    ordering = ['exposer__system__name']

class ModuleAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identification', {
            'fields': ('system', 'name',  'external')
        }),
        ('Detail', {
            'classes': ('collapse',),
            'fields': ('goal','criticity','referents', 'documentation')
        }),
    )

    list_display = ['system', 'name', 'goal', 'external']
    list_display_links = ['name']
    
    search_fields = ['system__name','name', 'goal','referents', 'documentation']
    inlines = [InlineInterface, InlineDependency]

class SystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'referents', 'documentation', 'external']
    search_fields = ['name', 'description','referents', 'documentation']
    
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
    search_fields = ['exposer__name', 'name','referents', 'documentation']

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
    search_fields = ['exposer__name', 'interface__name', 'interface__goal', 'technology', 'interface__documentation', 'interface__referents','referents', 'documentation']

admin.site.register(models.System, SystemAdmin)
admin.site.register(models.Module, ModuleAdmin)
admin.site.register(models.Interface, InterfaceAdmin)
admin.site.register(models.Dependency, DependencyAdmin)
