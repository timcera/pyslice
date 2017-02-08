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

pkgname = 'pyslice'
modname = 'setup.py'
version = open("VERSION").readline().strip()
exec_prefix = sys.exec_prefix

install_requires = [
        'six',
        ]
#=============================

#----------------------
setup(  # ---meta-data---
    name="pyslice",
    version=version,
    description="Pyslice is a templating engine to easily create data sets for parametric modeling.",
    long_description=readme + '\n\n' + history,

    author="Tim Cera, P.E.",
    author_email="tim@cerazone.net",
    url="http://timcera.bitbucket.org/pyslice/docsrc/index.html",
    install_requires=install_requires,
    packages=['pyslice',
        'pyslice.pyslice_lib',
        'pyslice.pyslice_lib.PySPG'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts':
            ['pyslice=pyslice:main']
        },
    classifiers=[
          # Get strings from
          # http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Science/Research',
          'Intended Audience :: End Users/Desktop',
          'Environment :: Console',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering',
          'Topic :: Text Processing :: General',
      ],
    )
#==============================
