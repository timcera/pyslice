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

    Additional commands:
    test                run the test suite
    doc                 build the documents

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

#--------------------
def debug(ftn,txt):
    sys.stdout.write(modname+'.'+ftn+':'+txt+'\n')
    sys.stdout.flush()
    
#--------------------
def fatal(ftn,txt):
    sys.stdout.write(string.join([modname,'.',ftn,':FATAL:',txt,'\n'],''))
    sys.stdout.flush()
    sys.exit(1)
#--------------------
def usage():
    print __doc__

#--------------------
def do_test():
    ftn="do_test"
    debug(ftn,"begin")
    os.system("cd test; go")

#----------------------
def do_doc():
    ftn="do_doc"
    debug(ftn,"begin")
    os.system("cd doc; go")

#----------------------
def main():
    setup (#---meta-data---
           name = "pyslice"
           ,version = version
           ,description = "pyslice"
           ,author = "Tim Cera"
           ,author_email = "timcera@earthlink.net"
           ,url="http://home.earthlink.net/~timcera"
           ,licence = "GPL"

           #---scripts,modules and packages---
           ,scripts=['pyslice.py']
##            ,py_modules = ['pyslice']
##            ,packages = ['']
##            ,package_dir = {'': ''}
##            ,ext_modules = 
##               [Extension('my_ext', ['my_ext.c', 'file1.c', 'file2.c'],
##                       include_dirs=[''],
##                       library_dirs=[''],
##                       libraries=[''],)
##                ]

           )
#==============================
if __name__ == '__main__':
    opts,pargs=getopt.getopt(sys.argv[1:],'hv',
                 ['help','version','exec-prefix'])
    for opt in opts:
        if opt[0]=='-h' or opt[0]=='--help':
            usage()
            sys.exit(0)
        elif opt[0]=='-v' or opt[0]=='--version':
            print modname+": version="+version
        elif opt[0]=='--exec-prefix':
            exec_prefix=opt[1]

    for arg in pargs:
        if arg=='test':
            do_test()
            sys.exit(0)
        elif arg=='doc':
            do_doc()
            sys.exit(0)
        else:
            pass

    main()
