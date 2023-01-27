import math
import os
import sys

import numpy as np


def loadData(s):
    with open(s) as fIn:
        return [
            list(map(float, strLine.replace("D", "E").strip().split()))
            for strLine in fIn.readlines()
            if strLine.find("nan") == -1
            and strLine.strip() != ""
            and strLine.find("inf") == -1
        ]


def dumpData(s, data):
    with open(s, "w") as fout:
        for line in data:
            fout.write("\t".join([str(i) for i in line]) + "\n")


def loadXY(s, xCol=0, yCol=1):
    data = loadData(s)
    out = []
    for line in data:
        try:
            out.append([line[xCol], line[yCol]])
        except:
            sys.stderr.write("skipping line %d, wrong size\n" % (data.index(line)))
    return out


#    return [
#           [line[xCol],line[yCol] ]
#           for line in data
#         ]
#  except:
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
#    sys.stderr.write("error!!! in file: %s...\n"%s)
#    sys.stderr.write("not enough columns, or inconsistent datafile. asked for columns %d and %d, where there are only %d..\n"%(xCol,yCol,len(data[0])))
#    sys.stderr.write("not enough columns, or inconsistent datafile. asked for columns %d and %d, where there are only %d..\n"%(xCol,yCol,len(data[-1])))
#    sys.stderr.write("gracefully quitting...\n")
#    sys.exit()


def loadXYZ(s, xCol=0, yCol=1, zCol=2):
    return [[line[xCol], line[yCol], line[zCol]] for line in loadData(s)]


def loadY(s, yCol=1):
    with open(s) as fIn:
        lines = fIn.readlines()

    try:
        ls = [float(line.strip().split()[yCol]) for line in lines if len(line) > 1]
        return ls
    except:
        sys.stderr.write(
            " ... error reading file: %s, %d\n"
            % (os.path.realpath(s), os.path.isfile(s))
        )
        return [0]


def transformXY(ls, xFormula="x", yFormula="y"):

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


def histogram(data, nbins, maxboxsize=10000, minx=-1e64, maxx=1e64):
    #
    # pythonize this code!!!!!!
    #
    if len(data) == 0:
        data = [0]

    mina = max(min(data), minx)
    maxa = min(max(data), maxx)
    boxsize = min(maxboxsize, ((maxa - mina) // nbins))
    out = [0] * int(math.ceil((maxa - mina) // boxsize))

    for idata in data:
        try:
            pos = int(math.floor((idata - mina) // boxsize))
            if pos == len(out):
                pos = len(out) - 1
            sys.stderr.write("%d\n" % pos)
            out[pos] += 1
        except:

            sys.stderr.write(f"histogram error!!! len(data) = {len(out)} \n")
            sys.stderr.write(
                "\n".join(
                    [
                        f"{str(k)} = {str(locals()[k])}"
                        for k in list(locals().keys())
                        if k != "data"
                    ]
                )
                + "\n"
            )

            sys.exit()
    suma = np.sum(out)

    out3 = [(x // suma) for x in out]
    out2 = []

    for i in range(nbins):
        out2.append([float(i) / float(nbins) * (maxa - mina) + mina, out3[i]])
    return out2
