"""
:::~ Author: Claudio Juan Tessone <tessonec@imedea.uib.es> (c) 2002-2005

Distributed According to GNU Generic Purpose License (GPL)
Please visit http://www.gnu.org
"""

# :::~ Important: for constants and functions already defined
import copy
import sys
from math import *

from . import ParamIterators


class ParamParser:
    """
    Initialized with a list of strings, each one containing commands.
    Each line will have a syntax as follows
    (iterator_type) (variable_name) [bounds]
    (iterator_type) can be one of the following characters
    '+' '-' '*' '/'  => all of them expect bounds given by [min_value]
                        [max_value] [step]
    '.'              => punctual iterator, (bounds) is in fact a (BLANK
                        separated) list with all the possible values
    ':'              => defines a CONSTANT (i.e. not iterable object)
    '#'              => repetition operator
    """

    # :::~ This variable specifies the list separator used while parsing
    # "param.dat"
    separator = " "

    # :::~ A dictionary with all the possible iterators
    iterator_types_dict = {
        "+": ParamIterators.ItOperatorPlus,
        "-": ParamIterators.ItOperatorMinus,
        "*": ParamIterators.ItOperatorProduct,
        "/": ParamIterators.ItOperatorDivision,
        "**": ParamIterators.ItOperatorPower,
        ":": ParamIterators.ItConstant,
        ".": ParamIterators.ItPunctual,
        "#": ParamIterators.ItRepetition,
    }

    # :::~ a list with an alternative order if your binary does not read
    # a free-style input file alternative_order = []
    # :::~ a list with all the varying entities (i.e. those not CONSTANT)
    # isvariable = []
    def __init__(self, lsLines):
        """
        lsLines is a list of commands understood by this class.
        """
        self.entities = []
        self.iterator_list = []
        self.variables_list = []
        self.actual_values = {}
        self.__parse(lsLines)

        self.reversed = copy.copy(self.iterator_list)
        self.reversed.reverse()
        self.reset()

    def __get_iteration_and_command(self, cadena):
        """
        returns the iteration type of a command. The iteration type is defined
        as the set of non alphanumeric characters at the beginning of the line
        """
        last_char = 0
        while not cadena[last_char].isalnum():
            last_char += 1
        return cadena[:last_char], cadena[last_char:]

    def __parse(self, ls):
        """
        internal function that parses the input
        """
        for sit in ls:
            # strips trailing and leading blanks
            # iteration type
            it_type, str_rest = self.__get_iteration_and_command(sit.strip())
            new_iterator = self.iterator_types_dict[it_type]()
            new_iterator.set_command(str_rest, self.separator)
            self.iterator_list.append(new_iterator)

        self.variables_list = [
            i_iter for i_iter in self.iterator_list if i_iter.is_variable()
        ]
        self.entities = [i_iter.get_varname() for i_iter in self.iterator_list]

    def __next__(self):
        """
        next() iterates over the possible values raising a StopIteration when
        the possible values are exhausted
        """
        if self.is_reset:
            self.is_reset = False
            return self.actual_values

        for i_iter in self.reversed:
            last_iterated = i_iter
            varname = i_iter.get_varname()
            try:
                self.actual_values[varname] = next(i_iter)

                break
            except StopIteration:
                self.actual_values[varname] = i_iter.reset()

                if last_iterated == self.iterator_list[0]:
                    raise StopIteration

        return self.actual_values

    # 1
    def reset(self):
        """
        This function resets the iterator to its starting point
        """
        for i_iter in self.iterator_list:
            i_iter.reset()
            self.actual_values[i_iter.get_varname()] = i_iter.get_value()
        self.is_reset = True

    def __iter__(self):
        return self

    def __str__(self):
        """
        defines how the actual value of the parameter set is printed out.
        A good candidate to be overwritten in inheriting classes.
        """
        thisstr = (
            "\n".join(
                [
                    f"{k}{self.separator}{self.actual_values[k]}"
                    for k in self.entities
                    if k
                ]
            )
            + "\n"
        )
        # :::~ replaces structures of the kind {var} by var-value, very useful
        # for generation of multiple output files.
        for i_iter in self.iterator_list:
            varname = i_iter.get_varname()
            thisstr = thisstr.replace(
                f"{varname}", f"{varname}-{self.actual_values[varname]}"
            )

        return thisstr

    def value_of(self, varn):
        """
        returns the actual value of the variable 'varn'
        """
        try:
            return self.actual_values[varn]
        except ValueError:

            sys.stderr.write(
                f"""'{varn}' not found among entities
"""
            )
            sys.exit()

    def set_order(self, new_order):
        """
        sets a new order for the output.
        May be a subset of the variables, but it can not be a superset
        useful if your program only reads a fixed input file
        """
        try:
            for i in new_order:
                [k.get_varname() for k in self.iterator_list].index(i)
        except ValueError:
            sys.stderr.write(
                f"""error! {i} not found among entities
entities = {self.entities}"""
            )
            sys.exit()
        self.entities = new_order

    # 1
    def directory_tree(self, limit=-1):
        """
        returns the directory path conducting to the actual values of the
        parameter set.  by default (limit=-1) the directory tree is extended to
        all the variables list except for the last variable.

        By setting limit to something else, you change the amount of variables
        kept left from the directory generation. (i.e. limit=-2, will leave out
        of the directory path the last two variables)

        """

        import os.path

        thepath = os.path.curdir + os.path.sep

        for i_iter in self.variables_list[:limit]:
            thepath += "{}-{}{}".format(
                i_iter.get_varname(),
                self.actual_values[i_iter.get_varname()],
                os.path.sep,
            )

        return thepath

    # 1
    def output_tree(self, limit=-1):
        """
        returns the output from limit given the actual values of the parameter set.
        by default (limit=-1) the output will only print the last variable value.
        By setting limit to something else, you change the amount of variables printed
        (i.e. limit=-2, will print the value of the last two variables)
        """
        theoutput = ""
        for i_iter in self.variables_list[limit:]:
            theoutput += f"{self.actual_values[i_iter.get_varname()]}" + self.separator
        return theoutput


#
#
if __name__ == "__main__":
    # command=[":a 0","*c 2 6 3",":filename {c}.dat","+d 5 9 4","#2",":end"]
    #  command=["*c 2 18 3"]
    command = [":a 0", "*c 2 6 3", ":filename {c}.dat", "+d 5 9 4", ":end"]
    #
    print(command)
    pp = ParamParser(command)
    for i in pp:
        print(pp)
