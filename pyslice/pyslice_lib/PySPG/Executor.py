#! /usr/bin/python
#
#
# :::~ Author: Claudio Juan Tessone <tessonec@imedea.uib.es> (c) 2002-2003
#
# Distributed According to GNU Generic Purpose License (GPL)
# Please visit www.gnu.org
################################################################################


import sys
import os.path
import os

from ParamParser import *
from math import *


class Executor(ParamParser):
   #
   # :::~ This variable specifies how many VARIABLEs will be kept off
   #      the directory heirarchy (NOTE THAT MUST HAVE A MINUS SIGN)
   #
   limit=-1
   #
   # :::~ This variable specifies that your prigram will understand correctly
   #      the print command inside the input of your program
   #
   printfixed=False
   def run(self,exename,outname="out.dat",inname="in.dat"):
     """
     runs the program 'exename', that receives its input from
     'inname'. Outputs in file 'outname'. This is done for the current 
     value of parameters (note that this class inherits ParamParser
     """

     cwd=os.path.abspath(".")

     way2=self.directory_tree(self.limit)
     try:
       if not os.path.isdir(way2):
         os.makedirs(way2)
     except:
       print "Error!! creating directory: '%s'"%way2
       sys.exit(1)
     
     
     os.chdir(way2)


     value="\t".join( [ str(j) for i,j in self.actual_values()[self.limit:] ] )

     fparam=open(inname,"w")

#     if self.printfixed:
#       fparam.write("print  %s\n"%value)
     fparam.write(str(self))
     fparam.close()
     
     fout=open(outname,"a")
     fout.write(value+"\t")
     fout.close()

     os.system( "%s >> %s"%(exename ,outname) )
     os.chdir(cwd)


   def doit(self,command,inname="in.dat",outfile="out.dat"):
     flag=True
     while flag:
       self.run(command,outfile,inname)
       flag=self.next()

######################################################################
######################################################################
######################################################################
######################################################################
