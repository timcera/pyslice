#! /usr/bin/python

import PyGrace


def loadData (s):
  fIn=open(s)

  return  [
            map(float,strLine.split())
            for strLine in fIn.readlines()
          ]

  return retValue

def loadXY (s,xCol=0,yCol=1):
  return [
           [line[xCol],line[yCol] ]
           for line in loadData(s)
         ]


def loadY (s,yCol=1):
  fIn=open(s)

  return [
           float(line.split()[yCol])
           for line in fIn.readlines()

         ]


def transformXY(ls,xFormula="x",yFormula="y"):
  xf=xFormula.replace("x","(x)")
  yf=yFormula.replace("y","(y)")

  return [
           [
             eval( xf.replace("x",str(line[0]))   ),
             eval( yf.replace("y",str(line[1]))   )
           ]
           for line in ls
         ]




