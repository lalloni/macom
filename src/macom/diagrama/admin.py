# -*- coding: utf-8 -*-

from django.contrib import admin
from macom.diagrama import models
from django.utils.translation import ugettext_lazy as _

class InlineInterface(admin.TabularInline):
    model = models.Interface
    fields = ['name', 'goal', 'technology']
    verbose_name = _('Interface expuesta')
    verbose_name_plural = _('Interfaces expuestas')
    extra = 0
            
class ModuleAdmin(admin.ModelAdmin):
    fields = ['system', 'name', 'goal', 'external', 'criticity', 'consumed' ]
    filter_horizontal = ['consumed']
    list_display = ['system', 'name', 'goal', 'external']
    list_display_links = ['name']
    search_fields = ['name', 'goal']
    inlines = [InlineInterface]

class SystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'external']
    
class InterfaceAdmin(admin.ModelAdmin):
    list_display = ['exposer', 'name', 'goal']
    list_display_links = ['name']
    ordering = ['exposer']
    search_fields = ['name']
    
admin.site.register(models.Interface, InterfaceAdmin)
admin.site.register(models.Module, ModuleAdmin)
admin.site.register(models.System, SystemAdmin)
