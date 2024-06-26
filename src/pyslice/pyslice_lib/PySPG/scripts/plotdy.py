import os.path
import sys

import PySPG

# Lee los labels de las columnas
from plotdyconf import col_contents, lastvar, xlabel

BASEDIR = os.path.expanduser("~/devel/")
sys.path.append(BASEDIR)

for kcol, kerr, colname in col_contents:
    p2 = PySPG.MultiAgrizer(open("param.dat").readlines(), lastvar)
    p2.xlabel = xlabel
    p2.ylabel = colname

    p2.plottype = "xydy"
    p2.ycol = kcol
    p2.zcol = kerr

    p2.doit(f"{str(kcol)}err.agr", "out.dat")
