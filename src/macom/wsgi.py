import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macom.settings")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
