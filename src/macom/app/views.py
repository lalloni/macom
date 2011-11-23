# -*- coding: UTF-8 -*-

from django.shortcuts import render_to_response
from django.conf import settings 

def script_template(request, script_name):
    return render_to_response(script_name, {'diagram_service_url' : settings.DIAGRAM_SERVICE_URL })

def app(request):
    return render_to_response('app.html')
