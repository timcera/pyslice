#! /usr/bin/python
#
#
# :::~ Author: Claudio Juan Tessone <tessonec@imedea.uib.es> (c) 2002-2003
#
# Distributed According to GNU Generic Purpose License (GPL)
# Please visit www.gnu.org
################################################################################

import PyGrace
import Load
from ParamParser import *
import sys, os.path

class MultiAgrizer:

   xcol=0
   ycol=1
   xformula="x"
   yformula="y"
   xlabel="x"
   ylabel="y"
   xscale="Normal"
   yscale="Normal"

   def __init__(self,comm,lastvar):

     commands= [ i.strip() for i in comm if ( i.strip()[0]!="#" and i.strip()!="")]
     #print commands
     
     pTmp=ParamParser(commands[:]);
     lastpos=pTmp.var.index(lastvar);


     self.parser_original=ParamParser(commands[:lastpos]);
     
     lastvarpos=commands.index(
                    filter (lambda x:x.strip()[0] in "+*.", commands).pop() 
		  )
     
     self.parser_last=ParamParser(commands[lastpos:lastvarpos]);

     self.act=self.parser_original.actual_values()
     
     #print self.act


   def next(self):
     self.act=self.parser_original.next()
     return self.act


   def agr(self,outname="out.agr",inname="out.dat"):
     actualDir=os.path.abspath(".")
     elpath=actualDir
     self.title=""

    ####################################################
    # Genera el path base, donde estara el agr
    #
     for actorig,actval in self.act:
      # self.title += ", %s=%s"%actorig
       if actorig in self.parser_original.isvariable:
         self.title += " %s=%s"%(actorig,actval)
         elpath+="/%s-%s"%(actorig,actval)
         try:
           if not os.path.exists(elpath):
             print "Error el path no existe",elpath
             raise TypeError, "Error"
         except:
           sys.exit()
    #
    #
    #####################################################
     #print elpath
     sys.stdout = open (elpath+"/"+outname,"w")

     g1=PyGrace.GraceDocument()

    #####################################################
    # Genera los paths donde estan los files
    #
     self.parser_last.reset()
     flag=True
     while flag:
       totalpath=elpath
       legend=""
       for actlast in self.parser_last.actual_values():
 	  if actlast[0] in self.parser_last.isvariable:
            legend += " %s=%s"%actlast
            totalpath+="/%s-%s"%actlast
       ls  = Load.loadXY(totalpath+"/"+inname,self.xcol,self.ycol)
       ls2 = Load.transformXY(ls,self.xformula,self.yformula)
       g1.set_data(ls2,legend)
       flag=self.parser_last.next()
       
     g1.autoscale()
     g1.set_labels(self.xlabel,self.ylabel)
     g1.set_scale(self.xscale,self.yscale)
     g1.set_title(self.title)
     g1.dump()
    #
    #
    #####################################################



   def doit(self,outname="out.agr",inname="out.dat"):

     self.agr(outname,inname)
     flag=True#self.next()
     while flag:
      self.agr(outname,inname)
      flag=self.next()

     self.parser_original.reset()

######################################################################
######################################################################
