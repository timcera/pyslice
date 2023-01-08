#
#  This script plots all the specified files
#  outputed by a {}-something directive in a recoursive-directory
#  But it does not plot the file PLOTS AN HISTOGRAM CONSTRUCTED
#  FROM THE SERIE
#

# Specifies the grace format of the x axis
#

xlabel = "\\f{Times-Italic}t\\sk"
#
# Specifies the name of the last variable considered
# before plotting
#

histvec = ["{size}.dat"]


# configuration File
inputFile = "param.dat"

#
# If the files containing the data have a time serie that must be differenced first
# set this to something different to zero
# if you want to construct the histogram only with the raw data of the
# file leave it as is
mustComputeDiference = 0


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


for histvar in histvec:
    p2 = Agrizer(open(inputFile).readlines())

    p2.xlabel = xlabel
    p2.ylabel = "\\f{Times-Italic}P\\f{}(%s\\f{}\\N)" % xlabel

    p2.dohist(histvar)
