'''
Created on 17/03/2011

@author: sebas
'''
import pydot
from diagrama.models import System, Interface
from django.core.urlresolvers import reverse
from django.conf import settings

toolbar = {
    True: {'img': '%s/img/maximize.jpg' % settings.MEDIA_ROOT, 'action': 'maximize', 'label': 'Maximizar'},
    False: {'img': '%s/img/minimize.jpg' % settings.MEDIA_ROOT, 'action': 'minimize', 'label': 'Minimizar'},
}

def __id(obj, prefix = None):
    return "%s%s%s" % (prefix if prefix else '', obj.__class__.__name__, obj.id)

def __label(s):
    return unicode(s).encode('utf-8')

def graph(name, minimized = [], closedlist = [], extra = {}, cleaned=False, show_related_systems=False):
    graph = pydot.Dot(name, **extra)
    consumers_toadd = []
    replace_by = {}
    closed = []
    omit = []
    related_systems= dict()
    
    systems = System.objects.order_by('id').all()
    
    for s in systems:
        related_systems[s.id] = list(set(map(lambda i: i.exposer.system.id, Interface.objects.filter(consumers__system__id=s.id))))
        
    for s in systems:
        isminimized = str(s.id) in minimized
        isclosed = str(s.id) in closedlist 
        
        if isclosed and s.id in related_systems[s.id] and show_related_systems:
            isclosed = False
        
        if cleaned:
            label = '"%s"' % (__label(s.name))
        else:
            label = '''<
            <table border='0'>
               <tr>
                  <td title='%s' href='%s'><img src='%s'/></td>
                  <td title='Cerrar' href='%s'><img src='%s/img/close.png'/></td>
                  <td width='10'></td>
                  <td width='300' align='left'><b>%s</b></td>
               </tr>
            </table>
            >''' % ( 
                    toolbar[isminimized]['label'], 
                    reverse(toolbar[isminimized]['action'],args=[s.id]), 
                    toolbar[isminimized]['img'], 
                    reverse('close', args=[s.id]),
                    settings.MEDIA_ROOT,
                    __label(s.name))
        
        if not isclosed:
            sub = pydot.Cluster(__id(s), lwidth='30', labeljust='l', color='red' if not s.external else 'orange', label=label, URL='"%s"'%s.get_absolute_url(), tooltip='Editar')
            graph.add_subgraph(sub)
        else:
            label = '''<
            <table border='0' title='Abrir' href='%s'><tr><td>%s</td></tr></table>
            >''' % (reverse('open', args=[s.id]), __label(s.name))
            closed.append(pydot.Node(__id(s), label=label, shape='plaintext'))

        modules = s.module_set.order_by('id').all()
        for m in modules:
            mod_node = pydot.Node(__id(m), label='"%s"'%__label(m.name), shape="component", URL='"%s"'%m.get_absolute_url())
            
            if not isclosed:
                if not isminimized :
                    sub.add_node(mod_node)
                else:
                    replace_by[__id(m)]= __id(s, 'cluster_')
            else:
                omit.append(__id(m))
                
            interfaces = m.exposed.order_by('id').all()
            for i in interfaces:
                int_node = pydot.Node(__id(i), shape="rect", URL='"%s"'%i.get_absolute_url(), label=__label(i.name))

                if not isclosed:
                    if not isminimized:
                        sub.add_node(int_node)
                        sub.add_edge(pydot.Edge(int_node, mod_node, arrowhead="none", arrowtail="none"))
                    else:
                        replace_by[__id(i)] = __id(s, 'cluster_')
                else:
                    omit.append(__id(i))
                
                consumers_toadd.append((i, i.consumers.order_by('id').all()))

    for i, consumers in consumers_toadd:
        idi = replace_by.get(__id(i), __id(i))
        for c in consumers:
            idc = replace_by.get(__id(c), __id(c))
            if idi not in omit and idc not in omit and idi != idc:
                graph.add_edge(pydot.Edge(idc, idi))

    if len(closed) > 0 and not cleaned:
        sub = pydot.Cluster('cluster_closed_systems', color='blue', label='Cerrados')
        graph.add_subgraph(sub)
        for c in closed:
            sub.add_node(c)

    return graph
