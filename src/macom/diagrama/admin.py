# -*- coding: utf-8 -*-

from django.contrib import admin
from macom.diagrama import models

class ModuleAdmin(admin.ModelAdmin):
    fields = ['system', 'name', 'goal', 'external', 'criticity', 'exposed', 'consumed' ]
    filter_horizontal = ['consumed', 'exposed']
    list_display = ['system', 'name', 'goal', 'external']

admin.site.register(models.Interface)
admin.site.register(models.Module, ModuleAdmin)
admin.site.register(models.System)
