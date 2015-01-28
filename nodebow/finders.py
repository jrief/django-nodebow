# -*- coding: utf-8 -*-
import os
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.staticfiles.finders import FileSystemFinder
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import SortedDict
from . import conf


class BowerComponentsFinder(FileSystemFinder):
    """
    Find static files installed with npm and/or bower
    """

    def __init__(self, apps=None, *args, **kwargs):
        bower_components = os.path.abspath(os.path.join(conf.PROJECT_PATH, 'bower_components'))

        if bower_components in getattr(settings, 'STATICFILES_DIRS', []):
            raise ImproperlyConfigured("The STATICFILES_DIRS setting should not contain the"
                                       "directory '{0}'".format(bower_components))
        if not os.path.isdir(bower_components):
            raise ImproperlyConfigured("The directory '{0}' does not exist".format(bower_components))
        self.locations = [
            ('', bower_components),
        ]
        self.storages = SortedDict()
        filesystem_storage = FileSystemStorage(location=bower_components)
        filesystem_storage.prefix = self.locations[0][0]
        self.storages[bower_components] = filesystem_storage
