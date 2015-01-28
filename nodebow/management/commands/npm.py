# -*- coding: utf-8 -*-
import os
import execjs
from django.core.management.base import CommandError
from nodebow import conf
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

    def install(self, node_settings):
        curdir = os.getcwd()
        self.stdout.write("Installing into {0}/node_modules".format(conf.PROJECT_PATH))
        os.chdir(conf.PROJECT_PATH)
        for app, settings in node_settings.items():
            dependencies = ['{0}#{1}'.format(p, v) for p, v in settings.get('dependencies', {}).items()]
            if self.verbosity > 0:
                self.stdout.write("Packages for {0}: {1}".format(app, ', '.join(dependencies)))
            retval = self.npm('install', dependencies)
            print retval
            if self.development:
                dependencies = ['{0}#{1}'.format(p, v) for p, v in settings.get('devDependencies', {}).items()]
                retval = self.npm('install', dependencies)
                print retval
        os.chdir(curdir)
