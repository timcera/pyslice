import os.path
import sys

#
#:::~ Author: Claudio J. Tessone <tessonec@imedea.uib.es>
#:::~ Release: Jan 10 2005
#:::~ Distributed under GNU/GPL License
#


#
# WARNING YOU MUST SPECIFY THE DIRECTORY WHERE PySPG LIVES
PySPGPATH = "~/devel/"
#
# name of the executable that has the main simulation loop
execFile = "ct-ordprm-kuramoto"
# name of the file expected by the executable for its input
inConfFile = "in.kmoto"
# PySPG configuration file
paramFile = "param.dat"

readCIN = False

# Checks whether the PySPG path exists, and adds it to the PATH
try:
    os.path.isdir(PySPGPATH)
    sys.path.append(os.path.expanduser(PySPGPATH))
except:
    sys.stderr.write(f"Error! '{PySPGPATH}' directory NOT FOUND\n")
    sys.exit(2)


# imports the PySPG library
try:
    from PySPG import *
except:
    sys.stderr.write("Couldn't import PySPG package, check PySPGPATH variable\n")
    sys.stderr.write("And verify that PySPG lives there\n")
    sys.stderr.write(f"actual value: '{PySPGPATH}'\n")

    sys.exit(2)

# reads the PySPG parameter file
try:
    lsLines = open(paramFile).readlines()
except:
    sys.stderr.write(f"Error! Couldn't open '{paramFile}' file\n")
    sys.exit(2)


# All the PySPG is done here!
xcutor = Executor(lsLines)
xcutor.doit(execFile, inConfFile, "out.dat")
