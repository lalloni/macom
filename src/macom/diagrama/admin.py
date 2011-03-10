# -*- coding: utf-8 -*-

from django.contrib import admin
from macom.diagrama import models

class ConsumedInterfaceInline(admin.TabularInline):
    verbose_name = 'Interfaz consumida'
    verbose_name_plural = 'Interfaces consumidas'
    model = models.ConsumedInterface
    fk_name = 'module'
    fields = ['name', 'criticity', 'contrapart', 'goal', 'technology', 'volume']
    extra = 0

class ExposedInterfaceInline(admin.TabularInline):
    verbose_name = 'Interfaz expuesta'
    verbose_name_plural = 'Interfaces expuestas'
    model = models.ExposedInterface
    fk_name = 'module'
    fields = ['name', 'criticity', 'goal', 'technology', 'volume', 'clients']
    filter_horizontal = ['clients']
    extra = 0
    
    class Media:
        css = {
            "all": ("/static-media/css/prueba.css",)
        }
        
class SystemAdmin(admin.ModelAdmin):
    search_fields = ['name']
    fields = ['name', 'description']
    list_display = ('name', 'description')
    list_display_links = ('name', 'description')
    
class ModuleAdmin(admin.ModelAdmin):
    fields = ['name', 'system', 'goal', 'external']
    list_display = ('name', 'system', 'external')
    list_display_links = ('name', 'system', 'external')
    search_fields = ['name']
    prepopulated_fields = {"goal": ("name",)}
    inlines = [ExposedInterfaceInline, ConsumedInterfaceInline]

admin.site.register(models.System, SystemAdmin)
admin.site.register(models.Module, ModuleAdmin)
