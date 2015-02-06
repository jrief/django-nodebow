# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if hasattr(settings, 'NODE_PATH'):
    os.putenv('NODE_PATH', settings.NODE_PATH)
elif os.getenv('NODE_PATH') is None:
    # if NODE_PATH is not an environment variable, determine it by executing `npm` in the shell.
    import subprocess
    _node_path = subprocess.check_output('npm root -g', shell=True).strip()
    os.putenv('NODE_PATH', _node_path)

NODEBOW_ROOT = getattr(settings, 'NODEBOW_ROOT', getattr(settings, 'STATIC_ROOT', None))
if not NODEBOW_ROOT:
    raise ImproperlyConfigured("The settings variable 'STATIC_ROOT' must be set.")
