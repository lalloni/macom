'''
Created on 17/03/2011

@author: sebas
'''
import pydot
from django.conf import settings

toolbar = {
    True: {'img': '%s/img/maximize.jpg' % settings.MEDIA_ROOT, 'action': 'maximize', 'label': 'Maximizar'},
    False: {'img': '%s/img/minimize.jpg' % settings.MEDIA_ROOT, 'action': 'minimize', 'label': 'Minimizar'},
}

def __id(obj, prefix = None):
    return "%s%s%s" % (prefix if prefix else '', obj.__class__.__name__, obj.id)

def __label(s):
    return unicode(s).encode('utf-8')

def graph(name, minimized = [], show = [], extra = {}, cleaned=True):
    graph = pydot.Dot(name, **extra)
    consumers_toadd = []
    replace_by = {}
    universe = []
    
    for s in show:
        isminimized = s in minimized
        
        universe.append(s)
        
        cluster_attrs = {
             'lwidth': '30', 
             'labeljust': 'l', 
             'color': 'red' if not s.external else 'orange', 
             'label': '"%s"' % (__label(s.name)), 
             'URL': '"%s"'%s.get_absolute_url(), 
             'tooltip': 'Editar'
        }
        sub = pydot.Cluster(__id(s), **cluster_attrs)
        graph.add_subgraph(sub)

        modules = s.module_set.order_by('id').all()
        for m in modules:
            universe.append(m)

            node_attrs = {
                  'label': '"%s"'%__label(m.name), 
                  'shape': "component", 
                  'URL': '"%s"'%m.get_absolute_url()
            }
            mod_node = pydot.Node(__id(m), **node_attrs)
            
            if not isminimized :
                sub.add_node(mod_node)
            else:
                replace_by[__id(m)]= __id(s, 'cluster_')
                
            interfaces = m.exposed.order_by('id').all()
            for i in interfaces:
                universe.append(i)
                
                int_attrs = {
                     'shape': "rect", 
                     'URL': '"%s"'%i.get_absolute_url(), 
                     'label': '"%s"'%__label(i.name),
                }
                int_node = pydot.Node(__id(i), **int_attrs)

                if not isminimized:
                    sub.add_node(int_node)
                    sub.add_edge(pydot.Edge(int_node, mod_node, arrowhead="none", arrowtail="none"))
                else:
                    replace_by[__id(i)] = __id(s, 'cluster_')

                consumers_toadd.append((i, i.consumers.order_by('id').all()))

    for i, consumers in consumers_toadd:
        idi = replace_by.get(__id(i), __id(i))
        for c in consumers:
            idc = replace_by.get(__id(c), __id(c))
            if i in universe and c in universe and idi != idc:
                graph.add_edge(pydot.Edge(idc, idi))

    return graph
