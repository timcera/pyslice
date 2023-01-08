#
#  This script plots from a recursive-directory all the requested columns
#  plotting ONE COLUMN IN ONE FILE
#


#
# Specifies the grace format of the x axis
#

xlabel = "\\f{Symbol}g"
#
# Specifies the name of the last variable considered
# before plotting
#
lastvar = "size"
size = 3
#
# Specifies the columns to be plotted
# and its label (in grace format)
#

#
# The output of ct-sr-linfhn is special:
# the first __size__ columns give SNR
#
col_contents_snr = [([i + 1 for i in range(size)], "\\f{Times-Italic}SNR")]
# the second __size__ columns give SAF
col_contents_saf = [([i + 1 + size for i in range(size)], "\\f{Times-Italic}SAF")]
# the third __size__ columns give the jitter
col_contents_ns = [([i + 1 + 2 * size for i in range(size)], "\\f{Times-Italic}J")]

# the fourth __size__ columns give the number of spikes
col_contents_ns = [([i + 1 + 3 * size for i in range(size)], "\\f{Times-Italic}N\\sS")]

#  let's put all the contents together
col_contents = col_contents_snr + col_contents_saf + col_contents_ns

# configuration File
inputFile = "param.dat"


# WARNING YOU MUST SPECIFY THE DIRECTORY WHERE PySPG LIVES
PySPGPATH = "~/devel/"

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


for kcol, colname in col_contents:
    p2 = MultiAgrizer(open(inputFile).readlines(), lastvar)
    p2.xlabel = xlabel
    p2.ylabel = colname

    p2.plottype = "xy"
    p2.ycol = kcol
    p2.xscale = "Logarithmic"
    outname = f"{'-'.join([str(i) for i in kcol])}.agr"
    p2.doit(outname, "out.dat")
