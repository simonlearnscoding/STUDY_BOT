import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoproject.myproject.settings'

import django
django.setup()


#TODO: do I even still need this file??





