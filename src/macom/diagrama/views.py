# -*- coding: utf-8 -*-

'''
Created on 09/03/2011

@author: sebas
'''

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render_to_response
from diagrama.utils import graph
from pydot import graph_from_dot_data
from django.core.urlresolvers import reverse
import datetime

def maximize_all(request):
    request.session['minimized'] = {}

    return HttpResponseRedirect(reverse(detail))

def minimize(request, entity, id):
    minimized = request.session.get('minimized', {})
    minimized.setdefault(entity, []).append(str(id))
    request.session['minimized'] = minimized

    return HttpResponseRedirect(reverse(detail))

def maximize(request, entity, id):
    minimized = request.session.get('minimized', {})
    byentity = minimized.get(entity, None)
    if byentity is not None and str(id) in byentity:
        byentity.remove(str(id))
        request.session['minimized'] = minimized

    return HttpResponseRedirect(reverse(detail))
    
def detail(request):
    minimized = request.session.get('minimized', {})
    g = graph('systems', minimized, {'layout': 'fdp', 'size': '10'})
    ctx = {'cmap': g.create(format='cmapx'), 'mapname': 'systems', 'show_maximizeall': len(minimized) > 0}
    request.session['graph'] = g.to_string()
    
    return render_to_response("detail.html", ctx)

def png(request):
    if 'graph' not in request.session:
        return HttpResponseNotFound("Graph not found in session")
    
    g = graph_from_dot_data(request.session['graph'])
    response = HttpResponse(g.create(format='png'), content_type='image/png')
    response['Cache-Control'] = 'no-cache'
    return response

def download(request, size = '100'):
    minimized = request.session.get('minimized', {})
    g = graph('systems', minimized, {'layout': 'fdp', 'size': str(size)})
    return HttpResponse(g.create(format='png'), content_type='image/png')
