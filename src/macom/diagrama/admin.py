# -*- coding: utf-8 -*-

from django.contrib import admin
from macom.diagrama import models
from django.utils.translation import ugettext_lazy as _

class InlineInterface(admin.StackedInline):
    model = models.Interface
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('module', 'name')
        }),
        ('Detail', {
            'classes': ('collapse',),
            'fields': ('goal','technology','direction_inbound', 'direction_outbound', 'tags')
        }),
    )
    list_display = ['module', 'name', 'goal', 'technology']
    verbose_name = _('Interface')
    verbose_name_plural = _('Interfaces')

class InlineDependency(admin.StackedInline):
    model = models.Dependency
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('module','interface')
        }),
        ('Detail', {
            'classes': ('collapse',),
            'fields': ('goal','technology','direction_inbound', 'direction_outbound','functional_referents','implementation_referents', 'documentation')
        }),
    )
    list_display = ['interface', 'goal', 'functional_referents', 'implementation_referents', 'documentation']
    search_fields = ['module__name', 'name','functional_referents','implementation_referents', 'documentation','technology']
    ordering = ['module__system__name']

class InlineModuleTypeCase(admin.TabularInline):
    model = models.ModuleTypeCase
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('module','moduletype', 'annotation')
        }),
    )
    list_display = ['module','moduletype']
    list_display_links = ['mdule','moduletype']
    ordering = ['module__system__name']

    verbose_name = _('Type')
    verbose_name_plural = _('Types')

    search_fields = ['module__name', 'moduletype', 'annotation']

class InlineArchitecturalPatternCase(admin.TabularInline):
    model = models.ArchitecturalPatternCase
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('module','architecturalpattern', 'annotation')
        }),
    )
    list_display = ['module','architecturalpattern']
    list_display_links = ['module','architecturalpattern']
    ordering = ['module__system__name']

    verbose_name = _('Architectural Pattern')
    verbose_name_plural = _('Architectural Patterns')

    search_fields = ['module__name', 'architecturalpattern', 'annotation']

class ModuleAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identification', {
            'fields': ('system', 'name',  'external')
        }),
        ('Detail', {
            'classes': ('collapse',),
            'fields': ('goal','criticity','functional_referents','implementation_referents', 'documentation', 'tags')
        }),
    )

    list_display = ['system', 'name', 'goal', 'external']
    list_display_links = ['name']
    
    search_fields = ['system__name','name', 'goal','functional_referents','implementation_referents', 'documentation']
    inlines = [InlineInterface, InlineDependency, InlineModuleTypeCase, InlineArchitecturalPatternCase]

class SystemAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {
            'fields': ('name',  'description', 'functional_referents', 'implementation_referents', 'documentation', 'external', 'tags')
        }),
    )
    list_display = ['name', 'description', 'functional_referents', 'implementation_referents', 'documentation', 'external']
    search_fields = ['name', 'description','functional_referents','implementation_referents', 'documentation']
    
class InterfaceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identification', {
            'fields': ('module', 'name')
        }),
        ('Direction', {
            'classes': ('wide',),
            'fields': ('direction_inbound', 'direction_outbound')
        }),
        ('Detail', {
            'classes': ('collapse',),
            'fields': ('goal','technology','functional_referents','implementation_referents', 'documentation', 'tags'),
        }),
    )
    list_display = ['module', 'name', 'goal', 'functional_referents', 'implementation_referents', 'documentation']
    list_display_links = ['name']
    ordering = ['module__system__name']
    search_fields = ['module__name', 'name','functional_referents','implementation_referents', 'documentation']

class DependencyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identification', {
            'fields': ('module','interface')
        }),
        ('Direction', {
            'classes': ('wide',),
            'fields': ('direction_inbound', 'direction_outbound')
        }),
        ('Detail', {
            'classes': ('collapse',),
            'fields': ('goal','technology','loadestimate', 'functional_referents', 'implementation_referents', 'documentation')
        }),
    )
    list_display = ['module', 'interface', 'goal', 'functional_referents', 'implementation_referents', 'documentation']
    list_display_links = ['module']
    ordering = ['module__system__name']
    search_fields = ['module__name', 'interface__name', 'interface__goal', 'technology', 'interface__documentation','functional_referents','implementation_referents', 'documentation']

class ModuleTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
    )
    list_display = ['name', 'description']
    list_display_links = ['name']
    ordering = ['name']
    search_fields = ['name', 'description']

class ArchitecturalPatternAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'tags')
        }),
    )
    list_display = ['name', 'description']
    list_display_links = ['name']
    ordering = ['name']
    search_fields = ['name', 'description']

class ModuleTypeCaseAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('module','moduletype', 'annotation')
        }),
    )
    list_display = ['module','moduletype']
    list_display_links = ['module','moduletype']
    ordering = ['module__system__name']
    search_fields = ['module__name', 'moduletype', 'annotation']


class ArchitecturalPatternCaseAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('module','architecturalpattern', 'annotation')
        }),
    )
    list_display = ['module','architecturalpattern']
    list_display_links = ['module','architecturalpattern']
    ordering = ['module__system__name']
    search_fields = ['module__name', 'architecturalpattern', 'annotation']

admin.site.register(models.System, SystemAdmin)
admin.site.register(models.Module, ModuleAdmin)
admin.site.register(models.Interface, InterfaceAdmin)
admin.site.register(models.ModuleType, ModuleTypeAdmin)
admin.site.register(models.ArchitecturalPattern, ArchitecturalPatternAdmin)
admin.site.register(models.Dependency, DependencyAdmin)
admin.site.register(models.ModuleTypeCase, ModuleTypeCaseAdmin)
admin.site.register(models.ArchitecturalPatternCase, ArchitecturalPatternCaseAdmin)

