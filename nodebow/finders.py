# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.contrib.staticfiles.finders import FileSystemFinder
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import SortedDict


class BowerComponentsFinder(FileSystemFinder):
    """
    Find static files installed with npm and/or bower
    """
    locations = []

    def __init__(self, apps=None, *args, **kwargs):
        nodebow_root = getattr(settings, 'NODEBOW_ROOT', settings.STATIC_ROOT)
        bower_components = os.path.abspath(os.path.join(nodebow_root, 'bower_components'))
        if not os.path.isdir(bower_components):
            return
        self.locations = [
            ('', bower_components),
        ]
        self.storages = SortedDict()
        filesystem_storage = FileSystemStorage(location=bower_components)
        filesystem_storage.prefix = self.locations[0][0]
        self.storages[bower_components] = filesystem_storage
