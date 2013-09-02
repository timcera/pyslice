#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===configuration=============
import os, sys, re, getopt, shutil
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('CHANGES.rst').read().replace('.. :changelog:', '')

pkgname = 'Pyslice'
modname = 'setup.py'
version = open("VERSION").readline().strip()
exec_prefix = sys.exec_prefix
#=============================

#----------------------
setup(  # ---meta-data---
    name="Pyslice",
    version=version,
    description="Pyslice is a templating engine to easily create data sets for parametric modeling.",
    long_description=readme + '\n\n' + history,

    author="Tim Cera, P.E.",
    author_email="tim@cerazone.net",
    url="http://timcera.bitbucket.org",
    license="GPL2",

    packages=['pyslice',
        'pyslice/pyslice_lib',
        'pyslice/pyslice_lib/PySPG'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts':
            ['pyslice=pyslice:main']
        }
    )
#==============================
