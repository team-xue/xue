#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Project Xue
# customized manage file

# check if it's debug setting...
#from os.path import isfile

from django.core.management import execute_manager
import imp

#DEBUG = isfile('is_debug')

SETTINGS_MODULE_NAME = 'settings'  # 'settings_dbg' if DEBUG else 'settings'

try:
    imp.find_module(SETTINGS_MODULE_NAME) # Assumed to be in the same dir
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file '%s.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % (SETTINGS_MODULE_NAME, __file__, ))
    sys.exit(1)

settings = __import__(SETTINGS_MODULE_NAME)

if __name__ == "__main__":
    execute_manager(settings)


# vim:ai:et:ts=4:sw=4:sts=4:ff=unix:fenc=utf-8:
