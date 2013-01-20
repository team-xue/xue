import os
import sys

path = os.path.normpath(
           os.path.dirname(os.path.realpath(__file__))
           )
upperpath = os.path.normpath(os.path.join(path, '..'))

if upperpath not in sys.path:
    sys.path.append(upperpath)

if path not in sys.path:
    sys.path.append(path)
del path
del upperpath

os.environ['DJANGO_SETTINGS_MODULE'] = 'xue.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
