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

   
   def __init__(self,comm,var_name):
     """
     Systematically plots the data generated by comm considering var_name as the last one
     the following ones are generated in the same plot
     """
     self.xcol=0
     self.ycol=1
     self.zcol=2
     self.xformula="x"
     self.yformula="y"
     self.zformula="z"
     self.xlabel="x"
     self.ylabel="y"
     self.xscale="Normal"
     self.yscale="Normal"
     self.plottype = "xy"
     self.autoscale_vars="xy"
     self.xmin=0
     self.xmax=1
     self.xticks=0.2
     self.ymin=0
     self.ymax=1
     self.yticks=0.2
     self.title=""
     self.dictLabels=None
     
     
     commands= [ i.strip() for i in comm if ( i.strip()[0]!="#" and i.strip()!="")]
     #print commands
     
     pTmp=ParamParser(commands);
     try:
       lastvar_idx=pTmp.entities.index(var_name);
     except:
       sys.stdout=sys.stderr
       print "last_var= ",var_name
       print "var=",lastvar_idx
       print "exiting... -presumible error: last var you provided does not"
       print " exist among the variables-"
       sys.exit()   

     self.parser_original=ParamParser(commands[:lastvar_idx]);
     
     lastvarpos=commands.index(
                    filter (lambda x:x.strip()[0] in "+*/-.", commands).pop() 
	                  )
     
     self.parser_last=ParamParser(commands[lastvar_idx:lastvarpos]);
     
  

   def set_world(self,xmin,xmax,ymin,ymax,xticks=None,yticks=None):
     """
       sets the bounds for the 
     """
     self.xmin=xmin
     self.xmax=xmax
     self.ymin=ymin
     self.ymax=ymax
     self.xticks=xticks
     self.yticks=yticks

   def __agr(self,outname,inname):
     """
     for the actual values of the iterator self.parser_original, dumps a agr
     """
     cwd=os.path.abspath( os.path.curdir )
     ####################################################
     # Directory where the AGR will be located
     #
     thepath=self.parser_original.directory_tree(None) 
     #
     #####################################################
     
     os.chdir(thepath)
     fOut = open (outname,"w")
     
     g1=PyGrace.GraceDocument()
     #####################################################
     # Genera los paths donde estan los files
     #
     self.parser_last.reset()
     for i_state in self.parser_last:
        fname = self.parser_last.directory_tree(None)+inname
        legend=" ".join([
	        "%s=%s"%(key,i_state[key]) 
	        for key in i_state
        ])
#       print i_state

        if self.plottype=="xy":
          ls  = Load.loadXY(fname,self.xcol,self.ycol)
          ls2 = Load.transformXY(ls,self.xformula,self.yformula)
        if self.plottype in ["xydy","xydx"] :
          ls  = Load.loadXYZ(fname,self.xcol,self.ycol,self.zcol)
          ls2 = Load.transformXYZ(ls,self.xformula,self.yformula,self.zformula)
        g1.set_data(ls2,legend,self.plottype)
 
#        
     g1.set_labels(self.xlabel,self.ylabel)
     g1.set_scale(self.xscale,self.yscale)
     g1.set_title(self.title)
     g1.autoscale()
     g1.dump(fOut)
     #
     #
     #####################################################
 
     os.chdir(cwd)

   def doit(self,outname="out.agr",inname="out.dat"):
     """
     given the commands, for all the possible values, do the plotting according the given rules
     """
     
     for i in self.parser_original:
   #    print self.parser_original
       self.__agr(outname,inname)
      

######################################################################
######################################################################
