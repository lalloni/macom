'''
Created on 17/03/2011

@author: sebas
'''
import pydot
from diagrama.models import System

def __id(obj, prefix = None):
    return "%s%s%s" % (prefix if prefix else '', obj.__class__.__name__, obj.id)

def __label(str):
    return '"%s"'%str.encode('utf-8')

def graph(name, extra = {}):
    graph = pydot.Dot(name, **extra)
    
    graph.set_node_defaults(shape='component')
    
    systems = System.objects.order_by('id').all()
    for s in systems:
        sub = pydot.Cluster(__id(s), color='red', label=__label(s.description), URL='"%s"'%s.get_absolute_url())
        
        graph.add_subgraph(sub)
        
        modules = s.module_set.order_by('id').all()
        for m in modules:
            subsub = pydot.Cluster(__id(m), color='blue', label=__label(m.name), URL='"%s"'%m.get_absolute_url())
            sub.add_subgraph(subsub)
            interfaces = m.exposed.order_by('id').all()
            for i in interfaces:
                n = pydot.Node(__id(i), label=__label(i.name), URL='"%s"'%i.get_absolute_url())
                subsub.add_node(n)

                consumers = i.consumers.order_by('id').all()
                for c in consumers:
                    subsub.add_edge(pydot.Edge(__id(c, 'cluster_'), __id(i)))
    
    return graph