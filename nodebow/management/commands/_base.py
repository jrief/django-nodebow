# -*- coding: utf-8 -*-
import os
import json
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand as DjangoBaseCommand, CommandError
from django.utils.importlib import import_module


class BaseCommand(DjangoBaseCommand):
    option_list = DjangoBaseCommand.option_list + (
        make_option('--dev', action='store_true', dest='development', default=False,
            help="Install additional npm packages for development."),
    )

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity'))
        self.development = options.get('development')
        args = list(args)
        try:
            command = args.pop(0)
        except IndexError:
            raise CommandError("Usage: ./manage.py {0} <command>".format(self.handler))
        try:
            method = getattr(self, command)
        except AttributeError:
            raise CommandError("No such command: ./manage.py {0} {1}".format(self.handler, command))
        else:
            method(args)

    def _collect_settings(self, apps):
        """
        Iterate over given apps or INSTALLED_APPS and collect the content of each's
        settings file, which is expected to be in JSON format.
        """
        contents = {}
        if apps:
            for app in apps:
                if app not in settings.INSTALLED_APPS:
                    raise CommandError("Application '{0}' not in settings.INSTALLED_APPS".format(app))
        else:
            apps = settings.INSTALLED_APPS
        for app in apps:
            module = import_module(app)
            for module_dir in module.__path__:
                json_file = os.path.abspath(os.path.join(module_dir, self.json_file))
                if os.path.isfile(json_file):
                    with open(json_file, 'r') as fp:
                        contents[app] = json.load(fp)
        return contents
