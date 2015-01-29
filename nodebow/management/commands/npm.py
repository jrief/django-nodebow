# -*- coding: utf-8 -*-
import os
import execjs
from django.conf import settings
from django.core.management.base import CommandError
from ._base import BaseCommand


class NPM(object):
    compiled_js = execjs.compile("""
    var npm = require('npm');
    function install(packages) {
        // currently broken, because I don't know how to find .npmrc
        return npm.commands.install(packages);
    }
    """)

    def __call__(self, function, *args):
        try:
            self.compiled_js.call(function, *args)
        except execjs.ProgramError as err:
            raise CommandError("During 'npm {0}': {1}".format(function, err))


class Command(BaseCommand):
    handler = 'npm'
    json_file = 'packages.json'
    help = "Manage dependencies of node modules for all installed Django apps."

    def handle(self, *args, **options):
        raise CommandError('Currently not working')
        self.npm = NPM()
        super(Command, self).handle(*args, **options)

    def install(self, args):
        node_settings = self._collect_settings(args)
        if not os.path.isdir(settings.STATIC_ROOT):
            raise CommandError("The folder '{0}' does not exists")
        self.stdout.write("Installing into {0}".format(os.path.join(settings.STATIC_ROOT, 'node_modules')))
        curdir = os.getcwd()
        os.chdir(settings.STATIC_ROOT)
        for app, ndsets in node_settings.items():
            dependencies = ['{0}#{1}'.format(p, v) for p, v in ndsets.get('dependencies', {}).items()]
            if self.verbosity > 0:
                self.stdout.write("Packages for {0}: {1}".format(app, ', '.join(dependencies)))
            retval = self.npm('install', dependencies)
            print retval
            if self.development:
                dependencies = ['{0}#{1}'.format(p, v) for p, v in ndsets.get('devDependencies', {}).items()]
                retval = self.npm('install', dependencies)
                print retval
        os.chdir(curdir)
