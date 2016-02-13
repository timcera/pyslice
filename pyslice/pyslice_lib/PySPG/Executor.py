#! /usr/bin/python

from __future__ import print_function
from __future__ import absolute_import

#
#
# :::~ Author: Claudio Juan Tessone <tessonec@imedea.uib.es> (c) 2002-2005
#
# Distributed According to GNU Generic Purpose License (GPL)
# Please visit www.gnu.org
#

import sys
import os.path
import os

from .ParamParser import *
from math import *


class Executor:
    #
    # :::~ This variable specifies how many VARIABLEs will be kept off
    #      the directory heirarchy (NOTE THAT MUST HAVE A MINUS SIGN)
    #

    def __init__(self, lsLines):
        self.parser = ParamParser(lsLines)
        self.limit = -1

    #
    # :::~ This variable specifies that your prigram will understand correctly
    #      the print command inside the input of your program
    #
    def run(self, exename, outname="out.dat", inname="in.dat"):
        """
        runs the program 'exename', that receives its input from
        'inname'. Outputs in file 'outname'. This is done for the current
        value of parameters
        """

        cwd = os.path.abspath(os.path.curdir)

        way2 = self.parser.directory_tree(self.limit)

        try:
            if not os.path.isdir(way2):
                os.makedirs(way2)
        except:
            print("Error!! creating directory: '%s'" % way2)
            sys.exit(1)

        os.chdir(way2)

        fparam = open(inname, "w")
        fparam.write(str(self.parser))
        fparam.close()

        open(outname, "a").write(self.parser.output_tree(self.limit) + "\t")

        os.system("%s >> %s " % (exename, outname))

        os.chdir(cwd)

    def doit(self, command, inname="in.dat", outfile="out.dat"):
        """
          runs systematically command (which is a OS command or executable). In the correspondig directory
          inname is the input file for the command
          while outfile is the output file name
        """
        for i in self.parser:
            self.run(command, outfile, inname)


#
#
#
#
