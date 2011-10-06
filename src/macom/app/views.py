# Create your views here.
from django.shortcuts import render_to_response

def script_template(request, script_name):
    return render_to_response(script_name)

def app(request):
    return render_to_response('app.html')
