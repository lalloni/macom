# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from macom.diagrama.models import Module, Dependency, Interface, System
from django.http import HttpResponse
from django.shortcuts import render_to_response
from macom.settings import DIAGRAMS_CACHE_BASE

class SystemDetailView(DetailView):
    model = System
    def get_context_data(self, **kwargs):
        context = super(SystemDetailView, self).get_context_data(**kwargs)
        system = context['object']
        context['interfaces'] = Interface.objects.filter(module__system=system)
        context['dependencies'] = Dependency.objects.filter(module__system=system).exclude(interface__module__system=system)
        return context

class ModuleDetailView(DetailView):
    model = Module
    def get_context_data(self, **kwargs):
        context = super(ModuleDetailView, self).get_context_data(**kwargs)
        module = context['object']
        context['dependencies'] = Dependency.objects.filter(module=module)
        return context

class InterfaceDetailView(DetailView):
    model = Interface
    def get_context_data(self, **kwargs):
        context = super(InterfaceDetailView, self).get_context_data(**kwargs)
        interface = context['object']
        context['dependencies'] = Dependency.objects.filter(interface=interface)
        return context

def system_components_diagram(request, pk):    
    return render_to_response(
        'system_components_diagram.plantuml',
        {
         'object': System.objects.get(pk=pk),
         'cache_base': DIAGRAMS_CACHE_BASE,
        },
        mimetype='text/plain')
