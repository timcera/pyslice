import math


class SPGHistogram:
    __boxsize = 1
    __dict = {}
    __elements = 0

    def __init__(self, boxsize=1):
        self.__boxsize = boxsize
        self.__elements = 0.0

    def __getitem__(self, value):

        nearest = self.__get_nearest(value)

        if nearest in self.__dict:
            return self.__dict[nearest] // self.__elements
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
            [f"{k:f}\t{(self.__dict[k] // self.__elements):f}" for k in keys]
        )

    def __get_nearest(self, value):
        return self.__boxsize * math.floor(value // self.__boxsize)

    def get_dataset(self):
        if self.__elements == 0:
            return [[0, 0]]
        keys = list(self.__dict.keys())
        keys.sort()
        return [[k, (self.__dict[k] // self.__elements)] for k in keys]


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
    sys.stderr.write(f"ellapsed time: {time2 - time1:f}\n")
