#
#  This script plots all the specified files
#  outputed by a {}-something directive in a recoursive-directory
#

#
# Specifies the grace format of the x axis
#

xlabel = "\\f{Times-Italic}t"
#
# Specifies the name of the last variable considered
# before plotting
#
extension = "psd"
size = 3

histvec = ["%d{gama}.%s" % (i, extension) for i in range(size)]

# configuration File
inputFile = "param.dat"


# WARNING YOU MUST SPECIFY THE DIRECTORY WHERE PySPG LIVES
PySPGPATH = "/t/users1/tessonec/devel/"


import os.path
import sys

try:
    os.path.isdir(PySPGPATH)
    sys.path.append(os.path.expanduser(PySPGPATH))
except:
    sys.stderr.write(f"error! '{PySPGPATH}' directory NOT FOUND\n")
    sys.exit(2)

try:
    from PySPG import *
except:
    sys.stderr.write("couldn't import PySPG package, check PySPGPATH variable\n")
    sys.stderr.write("and verify that PySPG lives there\n")
    sys.stderr.write(f"actual value: '{PySPGPATH}'\n")

    sys.exit(2)


p2 = Agrizer(open(inputFile).readlines())

p2.xlabel = xlabel
p2.ylabel = "\\f{Times-Italic}P\\f{}(%s\\f{})" % xlabel
p2.yscale = "Logarithmic"
p2.doit(pattern=histvec)
