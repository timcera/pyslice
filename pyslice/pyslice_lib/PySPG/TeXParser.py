#! /usr/bin/python

from __future__ import print_function
from __future__ import absolute_import

import sys
import os.path
import os

from .ParamParser import *


class TeXParser(ParamParser):
    replacing_rules = {
        "\s": "_",
              "\S": "^",
              "\f{Symbol}": " ",
              "\\f{}": " ",
              "\\N": "   "
    }

    def __agr2tex(agr_str):
        ret = agr_str
        for i in replacing_rules:
            ret = ret.replace(i, replacing_rules[i])

        return ret

    def __init__(self, comm, var_name):

        commands = [i.strip()
                    for i in comm if (i.strip()[0] != "#" and i.strip() != "")]
        # print commands

        pTmp = ParamParser(commands)
        try:
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
            filter(
                lambda x: x.strip()[0] in "+*/-.", commands).pop()
        )

    def __tex(self, outname="plots.tex", plotnames=[]):
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
        fOut = open(outname, "w")

        os.system("~/opt/bin/cts-print.sh")
        cout = sys.stdout
        sys.stdout = fOut

        print("\\documentclass[12pt]{article}")
        print()
        print("\\usepackage{graphicx}")
        print()
        print("\\begin{document}")
        print()
        print()
        print("Gr\\'aficos generados con los siguientes par\\'ametros:")
        print("\\begin{itemize}")
        actual_values = self.parser_original.actual_values
        for i in actual_values:
            print("\\item    { \\tt",)
            if actual_values[i] == '':
                posunder = i.find("_")
                if posunder > 0:
                    posblank = i.find("0")
                    print("\\begin{verbatim}")
                    print(i,)
                    print("\\end{verbatim}")
                else:
                    print(i,)
            else:
                print(" $ %s = %s $" % (i, actual_values[i]),)
            print(""" }   """)
        print("\\end{itemize}")
        print()
        print()
        ac_floats = 0
        for i in plotnames:
            print("\\begin{figure}[!ht]")
            print("\\begin{center}")
            print("\\includegraphics[height=10cm,angle=-90]{%s.eps}" % (i))
            print("\\end{center}")
            print("\\end{figure}")
            ac_floats += 1
            if ac_floats % 12 == 0:
                print("\\clearpage")

        print("\\end{document}")
        fOut.close()
        sys.stdout = cout
        os.system("latex %s" % outname)
        comandoexec = "dvips -o %s.ps  %s" % (
            os.path.splitext(outname)[0], os.path.splitext(outname)[0] + ".dvi")
        print(comandoexec)
        os.system(comandoexec)

        os.chdir(cwd)

    def doit(self, outname="plots.tex", plotnames=[]):
        """
         Suquencially dumps all the plotnames (a list of .agr files)
        """
        for i in self.parser_original:
            self.__tex(outname, plotnames)
