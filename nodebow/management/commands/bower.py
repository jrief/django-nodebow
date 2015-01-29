# -*- coding: utf-8 -*-
import os
import execjs
from django.conf import settings
from django.core.management.base import CommandError
from ._base import BaseCommand


class Bower(object):
    compiled_js = execjs.compile("""
    var bower = require('bower');
    function install(packages) {
        return bower.commands.install(packages);
    }
    """)

    def __call__(self, function, *args):
        try:
            self.compiled_js.call(function, *args)
        except execjs.Error as err:
            raise CommandError("During 'bower {0}': {1}".format(function, err))


class Command(BaseCommand):
    handler = 'bower'
    json_file = 'bower.json'
    help = "Manage dependencies of bower components for all installed Django apps."

    def handle(self, *args, **options):
        self.bower = Bower()
        super(Command, self).handle(*args, **options)

    def install(self, args):
        bower_settings = self._collect_settings(args)
        if not os.path.isdir(settings.STATIC_ROOT):
            raise CommandError("The folder '{0}' does not exists")
        self.stdout.write("Installing into {0}".format(os.path.join(settings.STATIC_ROOT, 'bower_components')))
        curdir = os.getcwd()
        os.chdir(settings.STATIC_ROOT)
        for app, bwsets in bower_settings.items():
            dependencies = ['{0}#{1}'.format(p, v) for p, v in bwsets.get('dependencies', {}).items()]
            if self.verbosity > 0:
                self.stdout.write("Packages for {0}: {1}".format(app, ', '.join(dependencies)))
            self.bower('install', dependencies)
            if self.development:
                dependencies = ['{0}#{1}'.format(p, v) for p, v in bwsets.get('devDependencies', {}).items()]
                self.bower('install', dependencies)
        os.chdir(curdir)
