#
#:::~ Author: Claudio J. Tessone <tessonec@imedea.uib.es>
#:::~ Release: Wed Oct  1 20:27:38 CEST 2003
#:::~ Distributed under GNU/GPL License
#
#


columnX = 12

import os.path
import sys

#
# WARNING YOU MUST SPECIFY THE DIRECTORY WHERE PySPG LIVES
PySPGPATH = "~/devel/"
#
# If you do not plan to change the name of ther executable,
# you can specify it here (obvioulsy it is a string)
paramFile = "param.dat"


def usage():
    print(f"usage is: {sys.argv[0]} [options] executable")
    print()
    print(
        ' -f param-file.dat : Reads parameters from param-file.dat \n\t\t (by default, "param.dat") '
    )
    print(
        ' -i in-file.dat : The name of the file read by the executable \n\t\t(by default, "in.dat") '
    )
    print(" - : Reads parameters from standard input ")
    print("")
    print('Repetedly executes "executable". ', end=" ")
    print(
        'If you do not plan to change the name \nof the executable, you can directly modify the "execFile" variable \ninside this script'
    )
    print()
    print()


try:
    os.path.isdir(PySPGPATH)
    sys.path.append(os.path.expanduser(PySPGPATH))
except:
    sys.stderr.write(f"Error! '{PySPGPATH}' directory NOT FOUND\n")
    sys.exit(2)

try:
    from PySPG import *
except:
    sys.stderr.write("Couldn't import PySPG package, check PySPGPATH variable\n")
    sys.stderr.write("And verify that PySPG lives there\n")
    sys.stderr.write(f"actual value: '{PySPGPATH}'\n")

    sys.exit(2)

try:
    lsLines = open(paramFile).readlines()
except:
    sys.stderr.write(f"Error! Couldn't open '{paramFile}' file\n")
    sys.exit(2)


for i in range(1, 9):
    print(i)
    mc = MeanCalculation(lsLines)
    mc.doit("out.dat", 0, i)
