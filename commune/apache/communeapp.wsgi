import os, sys
sys.path.append('/home/sites/ultimatehurl.com/commune')
sys.path.append('/home/sites/ultimatehurl.com/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'commune.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
