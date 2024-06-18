import os
import os.path
import sys

from .ParamParser import ParamParser


class TeXParser(ParamParser):
    replacing_rules = {
        r"\s": "_",
        r"\S": "^",
        "\f{Symbol}": " ",
        "\\f{}": " ",
        "\\N": "   ",
    }

    def __init__(self, comm, var_name):
        commands = [
            i.strip() for i in comm if (i.strip()[0] != "#" and i.strip() != "")
        ]
        # print commands

        pTmp = ParamParser(commands)
        try:
            lastvar_idx = pTmp.entities.index(var_name)
        except Exception:
            sys.stdout = sys.stderr
            print("last_var= ", var_name)
            print("var=", lastvar_idx)
            print("exiting... -presumible error: last var you provided does not")
            print(" exist among the variables-")
            sys.exit()

        self.parser_original = ParamParser(commands[:lastvar_idx])

        commands.index(filter(lambda x: x.strip()[0] in "+*/-.", commands).pop())

    def __tex(self, outname="plots.tex", plotnames=None):
        """
        for the actual values of the iterator self.parser_original, dumps a agr
        """
        if plotnames is None:
            plotnames = []
        cwd = os.path.abspath(os.path.curdir)
        #
        # Directory where the AGR will be located
        #
        thepath = self.parser_original.directory_tree(None)
        #
        #

        os.chdir(thepath)
        with open(outname, "w") as fOut:
            cout = self.__extracted_from___tex_17(fOut, plotnames)
        sys.stdout = cout
        os.system(f"latex {outname}")
        comandoexec = f"dvips -o {os.path.splitext(outname)[0]}.ps  {os.path.splitext(outname)[0]}.dvi"
        print(comandoexec)
        os.system(comandoexec)

        os.chdir(cwd)

    # TODO Rename this here and in `__tex`
    def __extracted_from___tex_17(self, fOut, plotnames):
        os.system("~/opt/bin/cts-print.sh")
        result = sys.stdout
        sys.stdout = fOut

        print("\\documentclass[12pt]{article}")
        print()
        print("\\usepackage{graphicx}")
        print()
        self.__extracted_from___tex_25("\\begin{document}")
        print("Gr\\'aficos generados con los siguientes par\\'ametros:")
        print("\\begin{itemize}")
        actual_values = self.parser_original.actual_values
        for i in actual_values:
            print("\\item    { \\tt")
            if actual_values[i] == "":
                posunder = i.find("_")
                if posunder > 0:
                    i.find("0")
                    print("\\begin{verbatim}")
                    print(i)
                    print("\\end{verbatim}")
                else:
                    print(i)
            else:
                print(f" $ {i} = {actual_values[i]} $")
            print(""" }   """)
        self.__extracted_from___tex_25("\\end{itemize}")
        for ac_floats, i in enumerate(plotnames, start=1):
            self.__extracted_from___tex_49(i, ac_floats)
        print("\\end{document}")
        return result

    # TODO Rename this here and in `__tex`
    def __extracted_from___tex_49(self, i, ac_floats):
        print("\\begin{figure}[!ht]")
        print("\\begin{center}")
        print("\\includegraphics[height=10cm,angle=-90]{%s.eps}" % (i))
        print("\\end{center}")
        print("\\end{figure}")
        if ac_floats % 12 == 0:
            print("\\clearpage")

    # TODO Rename this here and in `__tex`
    def __extracted_from___tex_25(self, arg0):
        print(arg0)
        print()
        print()

    def doit(self, outname="plots.tex", plotnames=None):
        """
        Suquencially dumps all the plotnames (a list of .agr files)
        """
        if plotnames is None:
            plotnames = []
        for _ in self.parser_original:
            self.__tex(outname, plotnames)
