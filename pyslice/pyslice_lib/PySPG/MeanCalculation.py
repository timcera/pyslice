#! /usr/bin/python
#
#
# :::~ Author: Claudio Juan Tessone <tessonec@imedea.uib.es> (c) 2002-2003
#
# Distributed According to GNU Generic Purpose License (GPL)
# Please visit www.gnu.org
################################################################################
#

import sys

class MeanCalculation(ParamParser):
   """
     When a simulation is run with a given number of repetitions what is needed is a
     tool for calculating the mean values
   """

   def __init__(self,lsLines):
     ls2=[
           i for i in lsLines
           if i.strip()[0] != "#"
         ]
     ParamParser.__init__(self,ls2)


   def searchinfile(self,fname,st):
     return [
               i.split()
               for i in open(fname,"r").readlines()
	       if i.split()[0]==st

	    ]


   def mean(self,fin_name="out.dat",ncol=2):

          dirname=self.directory_tree()
          acval=self.act_val(self.isvariable[-1])

   #  for acval in self.dc[self.isvariable[-1]]:
          fsearch="%s%s-%s/%s"%(dirname,self.isvariable[-1],acval,fin_name)

          try:
            col=load.loadY(fsearch,ncol)
          except:
	    print "Error! '%s' file doesn't exist or not enough permissions..."%fsearch
	    sys.exit()


          ac=0.
          for ic in col:
            ac+=ic


#          print self.isvariable[-1], " = ",acval
#          print  "%s%s.%.2d"%(dirname,fin_name,ncol)
          try:
            foutname="%s%s.%.2d"%(dirname,fin_name,ncol)
            open(foutname,"a").write("%s\t%s\n"%(acval,ac/len(col) ))
          except:
	    print "Error! Couldn't create file '%s' ..."%fsearch
	    sys.exit()






   def doit(self,fin_name="out.dat",ncol=2):
     flag=True
     while flag:
       self.mean()
       flag=self.next()

######################################################################
######################################################################
