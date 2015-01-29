======================================================
Manage Bower components and Node packages using Django
======================================================

Many Django applications require some JavaScript packages, which usually are not available on
[PyPI](https://pypi.python.org/pypi) and thus can't be installed through **pip**. A common
solution to this problem is, to copy these JavaScript packages into the Django application.
This however is a bad solution, since then these packages have to be revisioned twice. By
adding the file(s) ``bower.json`` and/or ``package.json`` to each Django application, this
problem can be solved in a portable and elegant manner.

With **django-nodebow** manage your JavaScript dependencies from *all* of your Django projects
centrally for the required bower components and/or node packages, simply through:

```
./manage.py bower install
# and/or
./manage.py npm install
```

The nice feature of **django-nodebow** is, that each Django application can specify which external
packages it requires itself, without adding these to its own Git repository.


Installation
============

Install [NodeJS](http://nodejs.org/download/).

Into your global NodeJS packages folder, install [bower](http://bower.io/):

```
sudo npm install -g bower inquirer
```

Into your Python virtualenv:

```
pip install django-nodebow
pip install PyExecJS
```


Configuration
=============

In ``settings.py``:

```
INSTALLED_APPS = (
    ...
    'nodebow',
    ...
)

STATICFILES_FINDERS = (
    ...
    'nodebow.finders.BowerComponentsFinder'
    ...
)
```


Optional settings
-----------------

By default, the folders ``bower_components`` and/or ``node_packages`` are placed into the
``STATIC_ROOT`` of your Django project. Therefore make sure, this directory is available, even
during development.

**NPM** searches for its global node modules in a folder, which can be set using the environment
variable ``NODE_PATH``. This can be overridden by a settings variable with the same name. If both
are unset, this location is determined by executing ``npm root -g`` in the shell.


Usage
=====

To install all the bower components which are required for your Django project, simply invoke:

```
./manage.py bower install
```

This will iterate over all applications defined in your ``INSTALLED_APPS`` settings, and look for a
file named ``bower.json``. If such a file was found, the list of ``dependencies`` is resolved and
the corresponding packages are installed into the folder ``bower_components`` of the local Django
project.

Say, one of the processed ``bower.json`` files contains an entry

```
  ...
  "dependencies": {
    ...
    "jquery": "~2.0.3",
    ...
  }
```

then, when accessing the main file, use

```
	{% load static %}
	...
	<script src="{% static 'jquery/jquery.js' %}" type="text/javascript"></script>
	...
```

in any of your Django templates.


As of version 0.0.1 ``./manage npm install``, currently does not work.

Difference between Bower and NPM
================================
**npm** is most commonly used for managing Node.js modules, which run exclusively on the
server-side.

**Bower** is created solely for the front-end and is optimized with that in mind. The biggest
difference is that npm does nested dependency tree (size heavy) while Bower requires a flat
dependency tree. This puts the burden of dependency resolution on the user.

A nested dependency tree means that your dependencies can have its own dependencies which can have
their own, and so on. This is really great on the server where you don't have to care much about
space and latency. It lets you not have to care about dependency conflicts as all your dependencies
use e.g. their own version of Underscore. This obviously doesn't work that well on the front-end.
Imagine a site having to download three copies of jQuery.

The reason many projects use both is that they use Bower for front-end packages and npm for
developer tools like SASS, LESS, Grunt, Gulp, JSHint, CoffeeScript, etc.
