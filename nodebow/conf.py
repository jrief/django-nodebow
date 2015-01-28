# -*- coding: utf-8 -*-
import os
from django.conf import settings

PROJECT_PATH = getattr(settings, 'PROJECT_PATH', os.path.abspath(os.path.dirname(__name__)))

if hasattr(settings, 'NODE_PATH'):
    os.putenv('NODE_PATH', settings.NODE_PATH)
elif os.getenv('NODE_PATH') is None:
    # if NODE_PATH is not an environment variable, determine it by executing `npm` in the shell.
    import subprocess
    _node_path = subprocess.check_output('npm root -g', shell=True).strip()
    os.putenv('NODE_PATH', _node_path)
