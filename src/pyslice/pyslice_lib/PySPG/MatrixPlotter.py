import os.path
import sys

from . import Load
from .ParamParser import *

#
#
# :::~ Author: Claudio Juan Tessone <tessonec@imedea.uib.es> (c) 2002-2003
#
# Distributed According to GNU Generic Purpose License (GPL)
# Please visit www.gnu.org
#


class MatrixPlotter:

    save_mtv = False

    def __init__(self, comm):
        self.xcol = 1
        self.xformula = "x"

        self.yformula = "y"

        self.zmin = None
        self.zmax = None
        self.nz = 50

        commands = [
            i.strip() for i in comm if (i.strip()[0] != "#" and i.strip() != "")
        ]
        try:
            pTmp = ParamParser(commands)
            var_name = pTmp.variables_list[-2].get_varname()
            print(var_name)
            lastvar_idx = pTmp.entities.index(var_name)
        except:
            sys.stdout = sys.stderr
            print("last_var= ", var_name)
            print("var=", lastvar_idx)
            print("exiting... -presumible error: last var you provided does not")
            print(" exist among the variables-")
            sys.exit()

        self.parser_original = ParamParser(commands[:lastvar_idx])

        lastvarpos = commands.index(
            filter(lambda x: x.strip()[0] in "+*/-.", commands).pop()
        )

        self.parser_last = ParamParser(commands[lastvar_idx:lastvarpos])

        self.iter2 = pTmp.variables_list[-2]
        self.iter1 = pTmp.variables_list[-1]

    def __matrix(self, outname, inname):
        """
        for the actual values of the iterator self.parser_original, dumps a agr
        """
        cwd = os.path.abspath(os.path.curdir)
        #
        # Directory where the AGR will be located
        #
        thepath = self.parser_original.directory_tree(None)
        #
        #

        os.chdir(thepath)
        #
        # Genera los paths donde estan los files
        #
        self.parser_last.reset()
        outputStr = ""
        for i_state in self.parser_last:
            fname = self.parser_last.directory_tree(None) + inname
            ls = Load.loadXY(fname, self.xcol, self.ycol)
            ls2 = [
                str(i[1]) for i in Load.transformXY(ls, self.xformula, self.yformula)
            ]
            outputStr += "\t".join(ls2) + "\n"
        #
        #
        #

        fOut = open(outname, "w")
        if self.save_mtv:
            mtvStr = f"""$ DATA=CONTOUR
% NX={len(self.iter1.data)}    XMIN={self.iter1.data[0]}   XMAX={self.iter1.data[-1]} XLABEL={self.iter1.get_varname()}
% NY={len(self.iter2.data)}    YMIN={self.iter2.data[0]}   YMAX={self.iter2.data[-1]} YLABEL={self.iter2.get_varname()}
% NSTEPS={self.nz}
"""
            if self.zmin is not None:
                mtvStr += f"""% ZMIN={self.cmin}
"""
            if self.zmax is not None:
                mtvStr += f"""% ZMAX={self.cmax}
"""
            mtvStr += """%contstyle=4
%interpolate=2
%contfill=True
"""

            fOut.write(mtvStr)

        fOut.write(outputStr)
        if self.save_mtv:
            mtvStr = "$ END"

            fOut.write(mtvStr)
        fOut.close()
        #     print outputStr
        os.chdir(cwd)

    def doit(self, outname="out.mtrx", inname="mean.dat", ycol=1):
        """
        given the commands, for all the possible values, do the plotting according the given rules
        """
        self.ycol = ycol
        for i in self.parser_original:
            #    print self.parser_original
            self.__matrix(outname, inname)


#
#
