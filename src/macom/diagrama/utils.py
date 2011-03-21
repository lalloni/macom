'''
Created on 17/03/2011

@author: sebas
'''
import pydot
from diagrama.models import System
from django.core.urlresolvers import reverse

def __id(obj, prefix = None):
    return "%s%s%s" % (prefix if prefix else '', obj.__class__.__name__, obj.id)

def __label(s):
    return '%s'%str(s).encode('utf-8')

def graph(name, minimized = {}, extra = {}):
    graph = pydot.Dot(name, **extra)
    
    #graph.set_node_defaults(shape='component')

    consumers_toadd = []
    replace_by = {}
    systems = System.objects.order_by('id').all()
    for s in systems:
        isminimized = str(s.id) in minimized.get('system', [])
        
        if isminimized:
            action = 'maximize'
            title = '^'
            desc = 'Maximizar'
        else:
            action = 'minimize'
            title = '_'
            desc = 'Minimizar'

        label = '''<
        <table cellpadding='0' cellborder='0' BORDER="0" cellspacing='0'>
           <tr>
              <td width="200" align="left"><b>%s</b></td>
              <td></td>
              <td title="%s" href="%s">%s</td>
           </tr>
        </table>
        >''' % (__label(s.name), desc, reverse(action,args=['system', s.id]) , title)
        
        sub = pydot.Cluster(__id(s), color='red' if not s.external else 'orange', label=label, URL='"%s"'%s.get_absolute_url())
        graph.add_subgraph(sub)

        modules = s.module_set.order_by('id').all()
        for m in modules:
            mod_node = pydot.Node(__id(m), label=__label(m.name), shape="component", URL='"%s"'%m.get_absolute_url())
    
            #print "Modulo: %s [%s]" % (m.id, isminimized)        
            if not isminimized:
                sub.add_node(mod_node)
            else:
                replace_by[__id(m)]= __id(s, 'cluster_')
                
            interfaces = m.exposed.order_by('id').all()
            for i in interfaces:
                int_node = pydot.Node(__id(i), shape="rec", URL='"%s"'%i.get_absolute_url(), label=__label(i.name))

                if not isminimized:
                    sub.add_node(int_node)
                    sub.add_edge(pydot.Edge(int_node, mod_node, arrowhead="none", arrowtail="none", style="dotted"))
                else:
                    replace_by[__id(i)] = __id(s, 'cluster_')
                
                consumers_toadd.append((i, i.consumers.order_by('id').all()))

    for i, consumers in consumers_toadd:
        for c in consumers:
            graph.add_edge(pydot.Edge(replace_by.get(__id(c), __id(c)), replace_by.get(__id(i), __id(i))))
                    
    print replace_by
    return graph