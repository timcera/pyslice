#! /usr/bin/python

from __future__ import print_function
from __future__ import absolute_import

#
#
# :::~ Author: Claudio Juan Tessone <tessonec@imedea.uib.es> (c) 2002-2003
#
# Distributed According to GNU Generic Purpose License (GPL)
# Please visit www.gnu.org
#
#

import sys
from math import *

from .Load import *
from .ParamParser import *
from six.moves import range


class MeanCalculation:

    """
      When a simulation is run with a given number of repetitions what is needed is a
      tool for calculating the mean values. This is that tool
    """

    def __init__(self, lsLines):
        ls2 = [
            i for i in lsLines
            if i.strip()[0] != "#"
        ]

        self.pp_varying = ParamParser(ls2)

    def searchinfile(self, fname, st):
        return [
            i.split()
            for i in open(fname, "r").readlines()
            if i.split()[0] == st

        ]

    def mean(self, fin_name="out.dat", fout_name="out.mean"):

        dirname = self.pp_varying.directory_tree()

        fsearch = "%s%s" % (dirname, fin_name)
        fout = "%s%s" % (dirname, fout_name)

        try:
            all_data = loadData(fsearch)
        except:
            print("Error! '%s' file doesn't exist or not enough permissions..." % fsearch)
            sys.exit()

        try:
            columnas = list(range(len(all_data[0])))
        except:

            sys.stderr.write("mean-> error! in directory '%s'\n" % dirname)
            sys.stderr.write("all_data = %s\n" % str(all_data))

        tmpDict = {}

        for i in all_data:
            tmpDict[i[0]] = 0
        valuesX = list(tmpDict.keys())
        valuesX.sort()

        xDict = {}
        nPoints = {}

        import copy
        zeros = [0 for i in columnas]

        for i in valuesX:
            xDict[i] = copy.copy(zeros)
            nPoints[i] = 0.

        for row in all_data:
            if len(row) == len(all_data[0]):
                nPoints[row[0]] += 1.
                vec = xDict[row[0]]
                for j in columnas:
                    vec[j] += row[j]

        dataOut = []

        for x in valuesX:
            if nPoints[x] != 0:
                dataOut.append(
                    [
                        xDict[x][j] / nPoints[x]
                        for j in columnas
                    ]
                )

        try:
            dumpData(fout, dataOut)
        except:
            print("Error! Couldn't create output file '%s' ..." % fsearch)
            sys.exit()

    def doit(self, fin_name="out.dat", fout_name="mean.dat"):
        for i in self.pp_varying:
            self.mean(fin_name, fout_name)


#
#
