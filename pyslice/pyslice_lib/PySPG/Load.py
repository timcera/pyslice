from __future__ import absolute_import
from __future__ import division

#! /usr/bin/python

from builtins import map
from builtins import str
from builtins import range
from past.utils import old_div
from . import PyGrace


def loadData(s):
    try:
        fIn = open(s)
    except:
        import sys

        sys.stderr.write("error!!! opening file: %s...\n" % s)
        sys.stderr.write("gently quitting...\n")
        sys.exit()
    try:
        return [
            list(map(float, strLine.replace("D", "E").strip().split()))
            for strLine in fIn.readlines()
            if strLine.find("nan") == -1
            and strLine.strip() != ""
            and strLine.find("inf") == -1
        ]
    except:
        import sys

        sys.stderr.write("error!!! in file: %s...\n" % s)
        sys.stderr.write("not correctly formatted, perhaps...\n")
        sys.stderr.write("gracefully quitting...\n")
        sys.exit()


def dumpData(s, data):
    try:
        fout = open(s, "w")
    except:
        import sys

        sys.stderr.write("error!!! opening for write file: %s...\n" % s)
        sys.stderr.write("gently quitting...\n")
        sys.exit()

    for line in data:
        fout.write("\t".join([str(i) for i in line]) + "\n")


def loadXY(s, xCol=0, yCol=1):
    data = loadData(s)
    out = []
    for line in data:
        try:
            out.append([line[xCol], line[yCol]])
        except:
            import sys

            sys.stderr.write("skipping line %d, wrong size\n" % (data.index(line)))
    return out


#    return [
#           [line[xCol],line[yCol] ]
#           for line in data
#         ]
#  except:
#    import sys
#    sys.stderr.write("error!!! in file: %s...\n"%s)
#    sys.stderr.write("not enough columns, or inconsistent datafile. asked for columns %d and %d, where there are only %d..\n"%(xCol,yCol,len(data[0])))
#    sys.stderr.write("not enough columns, or inconsistent datafile. asked for columns %d and %d, where there are only %d..\n"%(xCol,yCol,len(data[-1])))
#    sys.stderr.write("gracefully quitting...\n")
#    sys.exit()

# try: #
#    return [
#           [line[xCol],line[yCol] ]
#           for line in data
#         ]
#  except:
#    import sys
#    sys.stderr.write("error!!! in file: %s...\n"%s)
#    sys.stderr.write("not enough columns, or inconsistent datafile. asked for columns %d and %d, where there are only %d..\n"%(xCol,yCol,len(data[0])))
#    sys.stderr.write("not enough columns, or inconsistent datafile. asked for columns %d and %d, where there are only %d..\n"%(xCol,yCol,len(data[-1])))
#    sys.stderr.write("gracefully quitting...\n")
#    sys.exit()


def loadXYZ(s, xCol=0, yCol=1, zCol=2):
    return [[line[xCol], line[yCol], line[zCol]] for line in loadData(s)]


def loadY(s, yCol=1):
    fIn = open(s)
    import sys

    try:
        lines = fIn.readlines()
        #    sys.stderr.write("%d   ,"%len(lines) )
        ls = [float(line.strip().split()[yCol]) for line in lines if len(line) > 1]
        #    print len(ls)
        return ls
    except:
        import os.path

        sys.stderr.write(
            " ... error reading file: %s, %d\n"
            % (os.path.realpath(s), os.path.isfile(s))
        )
        #    sys.stderr.write("exiting...\n")
        #    sys.exit(2)
        return [0]


def transformXY(ls, xFormula="x", yFormula="y"):
    import math

    xf = xFormula.replace("x", "(x)")
    xf = xf.replace("y", "(y)")
    yf = yFormula.replace("x", "(x)")
    yf = yf.replace("y", "(y)")

    lsOut = []

    for line in ls:
        try:
            lsOut.append(
                [
                    eval(xf.replace("x", str(line[0])).replace("y", str(line[1]))),
                    eval(yf.replace("y", str(line[1])).replace("x", str(line[0]))),
                ]
            )

        except:
            import sys

            sys.stderr.write("skipping line: " + str(line) + "\n")
    return lsOut


def transformXYZ(ls, xFormula="x", yFormula="y", zFormula="z"):
    xf = xFormula.replace("x", "(x)")
    yf = yFormula.replace("y", "(y)")
    zf = zFormula.replace("z", "(z)")

    return [
        [
            eval(xf.replace("x", str(line[0]))),
            eval(yf.replace("y", str(line[1]))),
            eval(zf.replace("z", str(line[2]))),
        ]
        for line in ls
    ]


try:
    import numpy
except:
    import sys

    sys.stderr.write("numpy Package Not found...\n")
    sys.stderr.write("Not histogram capability present...\n")
else:

    def histogram(data, nbins, maxboxsize=10000, minx=-1e64, maxx=1e64):
        #
        # pythonize this code!!!!!!
        #
        if len(data) == 0:
            data = [0]
        import math

        mina = max(min(data), minx)
        maxa = min(max(data), maxx)
        #  mina=min(data)
        #  maxa=max(data)
        boxsize = min(maxboxsize, old_div((maxa - mina), nbins))
        out = [0] * int(math.ceil(old_div((maxa - mina), boxsize)))
        import sys

        for idata in data:
            try:
                pos = int(math.floor(old_div((idata - mina), boxsize)))
                if pos == len(out):
                    pos = len(out) - 1
                sys.stderr.write("%d\n" % pos)
                out[pos] += 1
            except:

                sys.stderr.write("histogram error!!! len(data) = %d \n" % len(out))
                sys.stderr.write(
                    "\n".join(
                        [
                            "%s = %s" % (str(k), str(locals()[k]))
                            for k in list(locals().keys())
                            if k != "data"
                        ]
                    )
                    + "\n"
                )

                sys.exit()
        suma = Numeric.sum(out)

        out3 = [old_div(x, suma) for x in out]
        out2 = []

        for i in range(nbins):
            out2.append([float(i) / float(nbins) * (maxa - mina) + mina, out3[i]])
        return out2
