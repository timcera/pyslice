from __future__ import absolute_import

#! /usr/bin/python

from builtins import str
import os.path

BASEDIR = os.path.expanduser("~/devel/")

import sys

sys.path.append(BASEDIR)

import PySPG

# Lee los labels de las columnas
from plotdyconf import *

for kcol, kerr, colname in col_contents:
    p2 = PySPG.MultiAgrizer(open("param.dat", "r").readlines(), lastvar)
    p2.xlabel = xlabel
    p2.ylabel = colname

    p2.plottype = "xydy"
    p2.ycol = kcol
    p2.zcol = kerr

    p2.doit(str(kcol) + "err.agr", "out.dat")
