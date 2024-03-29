# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView
from macom.diagrama.models import Module, Dependency, Interface, System
from django.shortcuts import render_to_response

class SystemDetailView(DetailView):
    model = System
    def get_context_data(self, **kwargs):
        context = super(SystemDetailView, self).get_context_data(**kwargs)
        system = context['object']
        context['interfaces'] = Interface.objects.filter(module__system=system)
        context['dependencies'] = Dependency.objects.filter(module__system=system).exclude(interface__module__system=system)
        context['dependents'] = Dependency.objects.filter(interface__module__system=system).exclude(module__system=system)
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

def system_diagram(request, pk):
    context = dict(
                   system=System.objects.get(id=pk),
                  )
    return render_to_response('diagrams/system.puml', context, mimetype="text/plain;charset=utf-8")

def module_diagram(request, pk):
    module = Module.objects.get(id=pk)
    dependencies = Dependency.objects.filter(module=pk).all()
    context = dict(
                   module=module,
                   dependencies=dependencies,
                   system_interfaces=Interface.objects.filter(module__system=module.system),
                   dependencies_interfaces=map(lambda dep: dep.interface, dependencies),
                  )
    return render_to_response('diagrams/module.puml', context, mimetype='text/plain;charset=utf-8')

def interface_diagram(request, pk):
    interface = Interface.objects.get(id=pk)
    context = dict(
                   interface=interface,
                   system_dependencies=Dependency.objects.filter(interface=interface, module__system=interface.module.system),
                   external_dependencies=Dependency.objects.filter(interface=interface).exclude(module__system=interface.module.system)
                  )
    return render_to_response('diagrams/interface.puml', context, mimetype="text/plain;charset=utf-8")

def dependency_diagram(request, pk):
    dependency = Dependency.objects.get(id=pk)
    context = dict(dependency=dependency)
    return render_to_response('diagrams/dependency.puml', context, mimetype="text/plain;charset=utf-8")

def unique_systems_dependencies(exclude_external=False):
    dependencies = []
    systems = System.objects.all()
    if exclude_external:
        systems = systems.filter(external=False)
    for system in systems:
        for module in system.modules.all():
            for dependency in module.dependencies.all():
                other = dependency.interface.module.system
                if system != other and not (exclude_external and other.external):
                    dependencies += [(system, other)]
    return (systems, set(dependencies))

def systems_dependencies_diagram(request):
    systems, dependencies = unique_systems_dependencies()
    context = dict(
                   systems=systems,
                   unique_dependencies=dependencies
                  )
    return render_to_response('diagrams/systems_dependencies.puml', context, mimetype="text/plain;charset=utf-8")

def systems_no_thirdparty_dependencies_diagram(request):
    systems, dependencies = unique_systems_dependencies(True)
    context = dict(
                   systems=systems,
                   unique_dependencies=dependencies
                  )
    return render_to_response('diagrams/systems_dependencies.puml', context, mimetype="text/plain;charset=utf-8")
