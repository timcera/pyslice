#! /usr/bin/python
version_number = "1.9.2"
release_date   = "Wed Sep 30 2003"
#
#
# :::~ Author: Claudio Juan Tessone <tessonec@imedea.uib.es> (c) 2002-2003
#
# Distributed According to GNU Generic Purpose License (GPL)
# Please visit www.gnu.org
################################################################################

import sys

from math import *


######################################################################
######################################################################
######################################################################
######################################################################

class ParamParser:
  """
    Initialized with a list of strings, each one containing commands
  """
  #
  #  :::~ This variable specifies the list separator used while
  #       parsing "param.dat"
  separator=" "
  
  def __init__(self,lsLines):
    self.dc = {}
    self.var = []
    self.isvariable = []

    self.__parse(lsLines)
    self.actual = [0 for i in  range(self.length)]



  def __parse(self,ls):
    for sit in ls:
      # strips trailing and leading blanks
      it=sit.strip()
      # iteration type
      it_type=it[0]

      if it_type in ['+','-','*','/'] :
        str_rest=it.split(self.separator)[1:]

        varname=str_rest[0].strip()
        try:
          [xmin,xmax,xstep]=map(eval,str_rest[1:])
        except:
          print "Line %d: "%(1+len(self.var)),
          print "incorrect number of parameters for iterator '%s' over '%s'"%(it_type,varname)
          sys.exit()
        #######################################
        #   Block that raises exception in the case that iteration requested
        #   do not reaches xmax

        try:
          if  ( xmin  < xmax ) and (xmin >= eval("%s %s %s" %(xmin,it_type,xstep) ) ) :
            raise AssertError,""

          if  ( xmin  > xmax ) and (xmin <= eval("%s %s %s" %(xmin,it_type,xstep) ) ) :
            raise AssertError, ""
        except:
          print "Line %d: "%(1+len(self.var)),
          print "Variable '%s': Error!"%varname, " ",xmin,it_type,xstep," no se aproxima a ",xmax

          sys.exit()
        #
        #######################################

        lsTmp=[]
        xact=xmin

        while((xmin>xmax) ^  (xact <= xmax) ): # ^ is xor in python !
          lsTmp.append(xact)
          xact=eval("%s%s%s"%(xact,it_type,xstep))

        self.dc[varname]=lsTmp
        self.var.append(varname)
        self.isvariable.append(varname)


      if it_type==":":
         varname=it[1:].strip()
         self.dc[varname]=[""]
         self.var.append(varname)

      if it_type==".":
         str_rest=it[1:].split(self.separator)
         varname=str_rest[0].strip()
         self.dc[varname]=[i.strip() for i in str_rest[1:] ]
         self.var.append(varname)
         self.isvariable.append(varname)


      if it_type=="#":
         self.var.append(False)
         try:
           self.dc[False]=range(eval (it[1:]) )
         except:
           print "Line %d: "%len(self.var)," iterator '#' could not eval  '%s'"%it[1:]
           sys.exit()

    self.length=len(self.var)


  def act_val(self,varn):
    index=self.var.index(varn)
    return self.dc[varn][self.actual[index]]


  def __poss_vals(self,idx):
    return self.dc[self.var[idx]]


  def __str__(self):
     return "\n".join( [
                         k.ljust(30)+"%s"%self.act_val(k)
                         for k in self.var
                         if k
                     ] )+"\n"


  def directory_tree(self,limit=-1):
    ac_values=self.actual_values()
    elpath="./"
    
    if type(limit)==type(1):
     for actual in ac_values:
       if actual[0] in self.isvariable[:limit]:
         elpath+="%s-%s/"%actual
    else:	 
     for actual in ac_values:
       if actual[0] in self.isvariable[:]:
         elpath+="%s-%s/"%actual
    return elpath




  def actual_values(self):
    """
      actual_values() return a list composed with the actual values generated
    """
    return [
#             (  k,self.dc[k][self.act_val(k)  ]  )
              (  k,self.act_val(k)  )
              for k in self.var if k
           ]


  def next(self):
    """
     next() iterates over the possible values returning None when the possible values
      are exhausted
    """
    changing_pos=self.length-1
    try:
      self.actual[changing_pos] = (self.actual[changing_pos]+1)%len(self.__poss_vals(changing_pos))
      while not self.actual[changing_pos] and changing_pos :
       changing_pos+=-1
       self.actual[changing_pos] = (self.actual[changing_pos]+1)%len(self.__poss_vals(changing_pos))
    except:
      print "Error! Iterating var # '%s'"%(changing_pos)
      sys.exit()


    if not ( changing_pos or max(self.actual) ) :
      return None;

    return self.actual_values()

  def reset(self):
    for i in range(len(self.actual)):
      self.actual[i]=0


######################################################################
######################################################################
