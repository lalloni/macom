# -*- coding: utf-8 -*-

'''
Created on 09/03/2011

@author: sebas
'''

from django.http import HttpResponse
from macom.diagrama.models import System
from pygraphviz.agraph import AGraph
from tempfile import NamedTemporaryFile
from django.shortcuts import render_to_response
import StringIO

def __id(obj):
    return "cluster_%s_%s" % (obj.__class__.__name__, obj.id)

def __graph():
    g = AGraph(name="systems", strict=False, directed=True)
    g.node_attr['shape'] = 'component'
   
    for s in System.objects.all():
        sub = g.add_subgraph('', __id(s), label=s.description.encode('utf-8'), color='red', href="http://www.google.com/%s"%s.name.encode('utf-8'))
        for m in s.module_set.all():
            sub_mod = sub.add_subgraph('', __id(m), label=m.name.encode('utf-8'), color='blue', href="http://www.google.com/%s"%m.name.encode('utf-8'))

            for i in m.exposed.all():
                sub_mod.add_node(__id(i), label=i.name.encode('utf-8'), href="http://www.google.com/%s"%i.name.encode('utf-8'))

                for c in i.consumers.all():
                    sub_mod.add_edge(__id(i), __id(c))
    return g

def detalle(request):
    #file = StringIO.StringIO()
    #g = __graph()
    #g.draw(path=file, format='cmapx', prog='fdp')
    #return render_to_response("detalle.html", {'cmap': file.getvalue(), 'mapid': str(g)})
    return render_to_response("detalle.html")

def png(request):
    file = NamedTemporaryFile(suffix='.png')
    g = __graph()
    g.draw(path=file.name, format='png', prog='fdp')
    dot = open(file.name).read()
    file.close()
    return HttpResponse(dot, content_type='image/png')
