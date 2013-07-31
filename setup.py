"""
NAME:
    setup.py

SYNOPSIS:
    python setup.py [options] [command]


DESCRIPTION:
    Using distutils "setup", build, install, or make tarball of the package.

OPTIONS:
    See Distutils documentation for details on options and commands.
    Common commands:
    build               build the package, in preparation for install
    install             install module(s)/package(s) [runs build if needed]
    install_data        install datafiles (e.g., in a share dir)
    install_scripts     install executable scripts (e.g., in a bin dir)
    sdist               make a source distribution
    bdist               make a binary distribution
    clean               remove build temporaries

    Additional options:
    --help              this message

EXAMPLES:
    cd mydir
    (cp myfile-0.1.tar.gz here)
    gzip -cd myfile-0.1.tar.gz | tar xvf -
    cd myfile-0.1
    python setup.py build
    python setup.py test
    python setup.py install
    python setup.py sdist
"""

#===configuration=============
import os,sys,re,getopt,shutil
from setuptools import setup

pkgname='Pyslice'
modname='setup.py'
version=open("VERSION").readline().strip()
exec_prefix=sys.exec_prefix
#=============================

#----------------------
setup (#---meta-data---
           name = "Pyslice"
           ,version = version
           ,description = "Pyslice is a templating engine to easily create data sets for parametric modeling."
           ,author = "Tim Cera"
           ,author_email = "tim@cerazone.net"
           ,url="http://timcera.bitbucket.org"
           ,license = "GPL"

           #---scripts,modules and packages---
           ,scripts=['pyslice.py']
##            ,py_modules = ['']
           ,packages = ['pyslice_lib'
                       ,'pyslice_lib/PySPG']

           )
#==============================
