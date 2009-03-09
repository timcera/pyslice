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
import os,sys,re,string,getopt,shutil,commands
from distutils.core import setup,Extension

pkgname='pyslice'
modname='setup.py'
version=string.strip(open("VERSION").readline())
exec_prefix=sys.exec_prefix
#=============================

#----------------------
setup (#---meta-data---
           name = "pyslice"
           ,version = version
           ,description = "pyslice"
           ,author = "Tim Cera"
           ,author_email = "timcera@earthlink.net"
           ,url="http://home.earthlink.net/~timcera"
           ,license = "GPL"

           #---scripts,modules and packages---
           ,scripts=['pyslice.py']
##            ,py_modules = ['']
           ,packages = ['pyslice_lib'
                       ,'pyslice_lib/PySPG']
##            ,package_dir = {'': ''}
##            ,ext_modules = 
##               [Extension('my_ext', ['my_ext.c', 'file1.c', 'file2.c'],
##                       include_dirs=[''],
##                       library_dirs=[''],
##                       libraries=[''],)
##                ]

           )
#==============================
