# -*- coding: utf-8 -*-
import os
import execjs
from django.core.management.base import CommandError
from nodebow import conf
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
        except execjs.ProgramError as err:
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
        curdir = os.getcwd()
        self.stdout.write("Installing into {0}/bower_components".format(conf.PROJECT_PATH))
        os.chdir(conf.PROJECT_PATH)
        for app, settings in bower_settings.items():
            dependencies = ['{0}#{1}'.format(p, v) for p, v in settings.get('dependencies', {}).items()]
            if self.verbosity > 0:
                self.stdout.write("Packages for {0}: {1}".format(app, ', '.join(dependencies)))
            retval = self.bower('install', dependencies)
            print retval
            if self.development:
                dependencies = ['{0}#{1}'.format(p, v) for p, v in settings.get('devDependencies', {}).items()]
                retval = self.bower('install', dependencies)
                print retval
        os.chdir(curdir)
