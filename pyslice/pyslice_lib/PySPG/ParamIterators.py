from __future__ import absolute_import
#
# :::~ Copyright (C) 2005 by Claudio J. Tessone <tessonec@imedea.uib.es>
#
# Created on: 09 Jan 2005
#
# Copyright: Distributed according to GNU/GPL Version 2
#            (see http://www.gnu.org)
#
#
import sys
from math import *

from six import Iterator
from six.moves import map
from six.moves import range


class SPGIterator(Iterator):

    """
    This is a subsidiary abstract class for the ParamParser one.  It defines the iteration type in the constructor. Must be subclassed (it's abstract)
    In principle there is no need to touch anything here (well, you can always improve the code) only you must subclass this object if you wish to add other iterator types
    """

    def __init__(self):
        self.index = 0
        self.varname = False
        self.data = []

    def __iter__(self):
        return self.data.__iter__()

    def is_variable(self):
        return True

    def set_command(self):
        """
        this is the function called to generate all the possible values of the iterator
        it returns the variable name and all the possible values it can take
        command holds the input line in the parameters file,
        separator is the character delimiting fields
        (if separator = None, any space is considered a separator)
        """
        pass

    def __next__(self):
        self.index += 1
        if self.index == len(self.data):
            raise StopIteration

        return self.data[self.index]

    def reset(self):
        self.index = 0
        return self.data[0]

    def get_varname(self):
        return self.varname

    def get_value(self):
        return self.data[self.index]


class ItOperator(SPGIterator):

    """
    This subclass generates the values for classes defined according to the rule
    @var_name val_min val_max step
    where @ is the operation defined for the data type.
    var_name is the variable name
    val_min, val_max the bounds
    step  the step
    the actualization process runs according to actual_value = actual_value @ step
    """

    def __init__(self, it_type):
        SPGIterator.__init__(self)
        self.it_type = it_type

    def set_command(self, command, separator=" "):
        str_rest = command.split(separator)
        self.varname = str_rest[0].strip()
        try:
            [xmin, xmax, xstep] = list(map(eval, str_rest[1:]))
        except:
            raise ValueError("Line: '{0}' incorrect number of parameters (found {1}) for iterator       '{2}' over '{3}'".format(
                command, len(str_rest) - 1, self.it_type, self.varname))
            #
            #   Block that raises exception in the case that iteration requested
            #   do not reaches xmax

        try:
            if (xmin < xmax) and (xmin >= eval("%s %s %s" % (xmin, self.it_type, xstep))):
                raise AssertError("")

            if (xmin > xmax) and (xmin <= eval("%s %s %s" % (xmin, self.it_type, xstep))):
                raise AssertError("")
        except:
            raise ValueError("Line: '{0}' Variable '{1}': Error! {2}{3}{4} do not seem to tend to {5}".format(
                command, self.varname, xmin, self.it_type, xstep, xmax))
        #
        #

        lsTmp = []
        xact = xmin

        while((xmin > xmax) ^ (xact <= xmax)):  # ^ is xor in python !
            lsTmp.append(xact)
            xact = eval("%s%s%s" % (xact, self.it_type, xstep))

        self.data = lsTmp


class ItOperatorPlus(ItOperator):

    def __init__(self):
        ItOperator.__init__(self, "+")


class ItOperatorMinus(ItOperator):

    def __init__(self):
        ItOperator.__init__(self, "-")


class ItOperatorProduct(ItOperator):

    def __init__(self):
        ItOperator.__init__(self, "*")


class ItOperatorDivision(ItOperator):

    def __init__(self):
        ItOperator.__init__(self, "/")


class ItOperatorPower(ItOperator):

    def __init__(self):
        ItOperator.__init__(self, "**")


class ItConstant(SPGIterator):

    """
    This subclass generates a constant "iteration" type
    """

    def __init__(self):
        SPGIterator.__init__(self)

    def is_variable(self):
        return False

    def set_command(self, command, separator=" "):
        self.varname = command.strip().split(separator)[0]
        self.data = [separator.join(command.strip().split(separator)[1:])]
        self.index = 0


class ItPunctual(SPGIterator):

    """
    This subclass generates a list of defined values in command
    command should be
    .var_name value1 value2 value3
    ... and so on
    """

    def __init__(self):
        SPGIterator.__init__(self)

    def set_command(self, command, separator=" "):
        str_rest = command.split(separator)
        self.varname = str_rest[0].strip()
#	 self.data = [eval (i.strip()) for i in str_rest[1:] ]
        self.data = [i.strip() for i in str_rest[1:]]


class ItRepetition(SPGIterator):

    """
    This subclass generates a list of null with length defined
    useful when trying to repit the run of the program with the same parameters
    """

    def __init__(self):
        SPGIterator.__init__(self)

    def set_command(self, command, separator=" "):
        try:
            self.varname = False
            self.data = list(range(eval(command)))
        except:
            raise ValueError(
                "Line: '{0}' iterator '#' could not eval()".format(command))
            sys.exit()

    def is_variable(self):
        return False
