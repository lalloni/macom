# -*- coding: utf-8 -*-
'''
Created on 17/03/2011

@author: sebas
'''
from subprocess import Popen
from tempfile import SpooledTemporaryFile
from pydot import graph_from_dot_data
from diagrama.models import System, Interface
import pydot

class PlantUML(object):
    COMPONENT = 'component'
    INTERFACE = 'interface'
    
    def __init__(self, jar, java = 'java'):
        self.jar = jar
        self.java = java
        self.code = ''
        
    def add(self, type, id, alias = None):
        self.code += ''' %s "%s" as %s\n ''' % (type, Utils.label(alias) if alias is not None else id, id)
    
    def relation(self, source, target, type = '--'):
        self.code += ''' %s %s %s\n ''' % (source, type, target)

    def graph(self):
        if self.code is '':
            return None
        
        stdin = SpooledTemporaryFile()
        stdout = SpooledTemporaryFile()

        stdin.write('@startuml\n')
        stdin.write(self.code)
        stdin.write('@enduml\n')
        
        stdin.seek(0)

        args = [
           self.java,
           '-jar',
           self.jar,
           '-p',
           '-tdot',
        ]

        p = Popen(args, stdin=stdin, stdout=stdout)

        if p.wait() != 0:
            return None

        stdout.seek(0)
        graph = stdout.read()
        return graph_from_dot_data(graph)
    
    def __l(self, s):
        return unicode(s).encode('utf-8')
    
class RawGraphViz(object):
    def __init__(self, show, minimized, related, extra={}):
        self.show = show
        self.minimized = minimized
        self.related = related
        self.extra = extra
        
    def graph(self):
        systems = System.objects.order_by('id').all()
        related_systems = dict()
        by_id = dict()
        
        for s in systems:
            related_systems[str(s.id)] = list(set(map(lambda i: i.exposer.system, Interface.objects.filter(consumers__system__id=s.id))))
            for i in Interface.objects.filter(exposer__system__id=s.id):
                related_systems[str(s.id)].extend(list(set(map(lambda c: c.system, i.consumers.all()))))
            by_id[str(s.id)] = s
    
        to_show = set()
        to_minimize = set()
        print "iterando show: %s" % self.show
        for s in self.show:
            to_show.add(by_id[str(s)])
        for s in self.minimized:
            to_minimize.add(by_id[str(s)])
        for s in self.related:
            to_show = to_show.union(related_systems[str(s)])
        
        self.extra['overlap'] = 'scaling'
        self.extra['ratio'] = 'expand'
    
        graph = pydot.Dot('systems', **self.extra)
        consumers_toadd = []
        replace_by = {}
        universe = []
        
        for s in to_show:
            isminimized = s in to_minimize
            
            universe.append(s)
            
            cluster_attrs = {
                 'lwidth': '30', 
                 'labeljust': 'l', 
                 'color': 'red' if not s.external else 'orange', 
                 'label': '"%s"' % (Utils.label(s.name)), 
                 'URL': '"%s"'%s.get_absolute_url(), 
                 'tooltip': 'Editar'
            }
            sub = pydot.Cluster(Utils.id(s), **cluster_attrs)
            graph.add_subgraph(sub)
    
            modules = s.module_set.order_by('id').all()
            for m in modules:
                universe.append(m)
    
                node_attrs = {
                      'label': '"%s"'%Utils.label(m.name), 
                      'shape': "component", 
                      'URL': '"%s"'%m.get_absolute_url()
                }
                mod_node = pydot.Node(Utils.id(m), **node_attrs)
                
                if not isminimized :
                    sub.add_node(mod_node)
                else:
                    replace_by[Utils.id(m)]= Utils.id(s, 'cluster_')
                    
                interfaces = m.exposed.order_by('id').all()
                for i in interfaces:
                    universe.append(i)
                    
                    int_attrs = {
                         'shape': "rect", 
                         'URL': '"%s"'%i.get_absolute_url(), 
                         'label': '"%s"'%Utils.label(i.name),
                    }
                    int_node = pydot.Node(Utils.id(i), **int_attrs)
    
                    if not isminimized:
                        sub.add_node(int_node)
                        sub.add_edge(pydot.Edge(int_node, mod_node, arrowhead="none", arrowtail="none"))
                    else:
                        replace_by[Utils.id(i)] = Utils.id(s, 'cluster_')
    
                    consumers_toadd.append((i, i.consumers.order_by('id').all()))
    
        for i, consumers in consumers_toadd:
            idi = replace_by.get(Utils.id(i), Utils.id(i))
            for c in consumers:
                idc = replace_by.get(Utils.id(c), Utils.id(c))
                if i in universe and c in universe and idi != idc:
                    graph.add_edge(pydot.Edge(idc, idi))
    
        return graph

class Utils(object):
    VIEWS = {
       'completo': 'Gráfico completo',
       'interfaces': 'Interfaces expuestas por sistema'
    }

    CONTENT_TYPES = {
         'png': 'image/png',
         'svg': 'image/svg+xml',
         'ps': 'application/postscript'
    }
    
    @staticmethod
    def id(obj, prefix = None):
        return "%s%s%s" % (prefix if prefix else '', obj.__class__.__name__, obj.id)

    @staticmethod
    def label(s):
        return unicode(s).encode('utf-8')
    
    @staticmethod
    def split(value, char=","):
        list = value.split(char) if str(value) is not "" and str(value) is not None else []
        return map(lambda x: x.strip(), list)

    @staticmethod
    def request_to_context(req):
        show, minimized, related = [], [], []
        for k in req.keys():
            Utils.add_if_starts_with('show', k, show)
            Utils.add_if_starts_with('minimized', k, minimized)
            Utils.add_if_starts_with('related', k, related)

        ctx = {
            'format': req.get('formato') if req.get('formato') else Utils.CONTENT_TYPES.keys()[0],
            'view': req.get('view') if req.get('view') else Utils.VIEWS.keys()[0],
            'show': Utils.serialize(show),         
            'minimized': Utils.serialize(minimized),
            'related': Utils.serialize(related),
        }
        return ctx

    @staticmethod
    def context(format, view, show, minimized, related):
        ctx = dict()
        ctx['mapname'] = 'systems'
        ctx['format'] = format if format else Utils.CONTENT_TYPES.keys()[0]
        ctx['view'] = view if view else Utils.VIEWS.keys()[0]
        ctx['show'] = show
        ctx['minimized'] = minimized
        ctx['related'] = related
        ctx['contenttypes'] = Utils.CONTENT_TYPES.keys()
        ctx['views'] = Utils.VIEWS.items()
        ctx['systems'] = list()
        ctx['empty'] = len(Utils.split(show, "_")) == 0
        
        systems = ctx['systems']
        show = Utils.split(show, "_")
        minimized = Utils.split(minimized, "_")
        related = Utils.split(related, "_")
        for s in System.objects.order_by('name').all():
            obj = {
                   'id': s.id, 
                   'name': s.name, 
                   'show': str(s.id) in show,
                   'minimized': str(s.id) in minimized,
                   'related': str(s.id) in related
            }
            systems.append(obj)
        return ctx
    
    @staticmethod
    def plantUML(systems):
        uml = PlantUML('/home/sebas/tmp/plantuml.jar')
        mappings = []
        for ids in systems:
            s = System.objects.get(id = ids)
            idc = 'C%s'%s.id
            uml.add(PlantUML.COMPONENT, idc, s.name)
            
            for i in Interface.objects.filter(exposer__system__id=s.id):
                idi = 'I%s'%i.id
                uml.add(PlantUML.INTERFACE, idi, i.name)
                mappings.append((idi, idc))
                
        for comp, iface in mappings:
            uml.relation(comp, iface)
            
        return uml.graph()
    
    @staticmethod
    def serialize(objs, sep="_"):
        return sep.join(objs)

    @staticmethod
    def add_if_starts_with(prefix, value, objs):
        if value.startswith(prefix):
            objs.append(value[len(prefix)+1:])
