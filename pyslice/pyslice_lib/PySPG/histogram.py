#! /usr/bin/python

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from builtins import range
from builtins import object
from past.utils import old_div
import math


class SPGHistogram(object):
    __boxsize = 1
    __dict = {}
    __elements = 0

    def __init__(self, boxsize=1):
        self.__boxsize = boxsize
        self.__elements = 0.0

    #    import sys
    #    sys.stderr.write("histogram box size = %lf\n"%self.__boxsize)

    def __getitem__(self, value):

        nearest = self.__get_nearest(value)

        if nearest in self.__dict:
            return old_div(self.__dict[nearest], self.__elements)
        else:
            return 0.0

    def add_value(self, value):
        nearest = self.__get_nearest(value)
        if nearest in self.__dict:
            self.__dict[nearest] += 1.0
        else:
            self.__dict[nearest] = 1.0
        self.__elements += 1.0

    def __str__(self):
        if self.__elements == 0:
            return " "
        keys = list(self.__dict.keys())
        keys.sort()
        return "\n".join(
            ["%f\t%f" % (k, (old_div(self.__dict[k], self.__elements))) for k in keys]
        )

    def __get_nearest(self, value):
        return self.__boxsize * math.floor(old_div(value, self.__boxsize))

    def get_dataset(self):
        if self.__elements == 0:
            return [[0, 0]]
        keys = list(self.__dict.keys())
        keys.sort()
        return [[k, (old_div(self.__dict[k], self.__elements))] for k in keys]


if __name__ == "__main__":
    a = SPGHistogram(0.1)
    import random
    import sys
    import time

    time1 = time.time()
    for i in range(100000):
        a.add_value(random.gauss(0.1, 0.5))
    time2 = time.time()

    print(a)
    sys.stderr.write("ellapsed time: %lf\n" % (time2 - time1))
