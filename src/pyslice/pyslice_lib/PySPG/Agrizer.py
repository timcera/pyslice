"""
#
# :::~ Author: Claudio Juan Tessone <tessonec@imedea.uib.es> (c) 2002-2003
#
# Distributed According to GNU Generic Purpose License (GPL)
# Please visit www.gnu.org
"""

import os
import os.path
import sys
from math import *

from . import Load, PyGrace
from .ParamParser import *


class Agrizer(ParamParser):
    box_size = 1.0
    min_value = None
    xcol = 0
    ycol = 1
    xformula = "x"
    yformula = "y"
    xlabel = "x"
    ylabel = "y"
    xscale = "Normal"
    yscale = "Normal"
    minx = 0.0
    maxx = 1.0
    miny = 0.0
    maxy = 1.0

    title = ""

    def agr(self, outname, inname):
        title = self.title
        elpath = ""
        ac_values = self.actual_values()
        for actual in ac_values:
            title += " %s=%s " % actual
            legend = " %s = %s " % actual

            if actual[0] in self.isvariable[:-1]:
                elpath += "%s-%s/" % actual

        try:
            if not os.path.exists(elpath):
                raise AssertionError("")
        except:
            print(f"Error accessing path: '{elpath}'.")
            sys.exit()
        cwd = os.getcwd()
        os.chdir(elpath)

        sys.stdout = open(outname, "w")

        ls = Load.loadXY(inname, self.xcol, self.ycol)
        ls2 = Load.transformXY(ls, self.xformula, self.yformula)

        g1 = PyGrace.GraceDocument()
        g1.set_data(ls2, legend)

        g1.autoscale()
        g1.set_labels(self.xlabel, self.ylabel)
        g1.set_scale(self.xscale, self.yscale)
        g1.set_title(title)
        g1.dump()

        os.chdir(cwd)

    def agr(self, pattern, outname=None, autoscale="xy"):

        title = self.title
        elpath = ""
        ac_values = self.actual_values()
        for actual in ac_values:

            if actual[0] in self.isvariable[:-1]:
                title += " %s=%s " % actual
                legend = " %s = %s " % actual
                elpath += "%s-%s/" % actual

        try:
            if not os.path.exists(elpath):
                raise AssertionError("")
        except:
            print(f"Error accessing path: '{elpath}'.")
            sys.exit()
        cwd = os.getcwd()
        os.chdir(elpath)
        if isinstance(pattern, str):
            pattern = [pattern]
        g1 = PyGrace.GraceDocument()
        for inname in pattern:
            for i in self.var:
                inname = inname.replace("{%s}" % i, f"{i}-{str(self.act_val(i))}")

            if os.path.isfile(inname):
                if not outname:
                    outname = f"{inname}.agr"

                else:
                    for i in self.var:
                        outname = outname.replace(f"{i}", f"{i}-{str(self.act_val(i))}")

                ls = Load.loadXY(inname, self.xcol, self.ycol)
                ls2 = Load.transformXY(ls, self.xformula, self.yformula)
                g1.set_data(ls2, legend)
                g1.set_labels(self.xlabel, self.ylabel)
                g1.set_scale(self.xscale, self.yscale)
                g1.set_title(title + inname)
                g1.set_world(self.minx, self.maxx, self.miny, self.maxy)
                g1.autoscale(autoscale)
                g1.autoscale()
                sys.stdout = open(outname, "w")
                g1.dump()

            else:
                sys.stderr.write(f"skipping {inname}... file does not exist\n")

        os.chdir(cwd)

    def hist(self, pattern, mustCalculateDif, outname=None, autoscale="xy"):

        title = self.title
        elpath = ""
        ac_values = self.actual_values()

        for actual in ac_values:

            if actual[0] in self.isvariable[:-1]:
                elpath += "%s-%s/" % actual
                title += " %s = %s " % actual

        legend = title
        cwd = os.getcwd()
        try:
            if not os.path.exists(elpath):
                raise AssertionError("")
        except:
            print(f"Error accessing path: '{elpath}'.")
            sys.exit()

        os.chdir(elpath)
        if isinstance(pattern, str):
            pattern = [pattern]
        g1 = PyGrace.GraceDocument()
        isSomething = 0  # false the document is void
        if not outname:
            outname = pattern[0]
        for i in self.var:
            outname = outname.replace("{%s}" % i, f"{i}-{str(self.act_val(i))}")

        for inname in pattern:
            for i in self.var:
                inname = inname.replace("{%s}" % i, f"{i}-{str(self.act_val(i))}")

            if os.path.isfile(inname):
                isSomething = 1  # true the document is NOT void

                ls = Load.loadY(inname, 0)
                if mustCalculateDif:

                    ls = [ls[i + 1] - ls[i] for i in range(len(ls) - 1)]
                from . import histogram

                hist = histogram.SPGHistogram(self.box_size)

                for x in ls:
                    hist.add_value(x)

                ls2 = hist.get_dataset()

                g1.set_data(ls2, legend, "bar")
            else:
                sys.stderr.write(f"skipping {inname}... file does not exist\n")
        if isSomething:
            sys.stdout = open(outname, "w")
            g1.set_labels(self.xlabel, self.ylabel)
            g1.set_scale(self.xscale, self.yscale)
            g1.set_title(title)
            g1.set_world(self.minx, self.maxx, self.miny, self.maxy)
            g1.autoscale(autoscale)
            g1.dump()
        os.chdir(cwd)

    def doit(
        self,
        outname="out.agr",
        inname="out.dat",
        pattern=None,
        patternname=None,
        autoscale="xy",
    ):
        flag = 1

        while flag:
            if not pattern:
                self.agr(outname, inname)
            else:
                self.agr(pattern, patternname)

            flag = next(self)
        self.reset()

    def dohist(self, pattern, mustCalculateDif=0, patternname=None, autoscale="xy"):
        flag = 1

        while flag:
            self.hist(pattern, mustCalculateDif, patternname)
            flag = next(self)
        self.reset()
