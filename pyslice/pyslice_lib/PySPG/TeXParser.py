#! /usr/bin/python

import sys
import os.path, os

from ParamParser import *

def agr2tex(agr_str):
  ret=agr_str.replace("\s","_")
  ret=ret.replace("\S","^")  
  ret=ret.replace("\\f{Symbol}"," ")  
  ret=ret.replace("\\f{}"," ")  
  ret=ret.replace("\\N","  ")  
  
  return ret


class TeXParser(ParamParser):

   def __init__(self,commands,lastvar):
     pTmp=CTParamParser(commands[:]);

     lastpos=pTmp.comandos.index(
                  filter(lambda x: x[0]==lastvar, pTmp.comandos).pop()
	     );   

     lastvarpos=commands.index(
                    filter (lambda x:x[:1] in "+*.", commands).pop() 
		  )

     self.parser_original=CTParamParser(commands[:lastpos]);
     self.parser_last=CTParamParser(commands[lastpos:lastvarpos]);
     self.act=self.parser_original.act
     
   def next(self):
     self.act= self.parser_original.next()
     return self.act
   
   def tex(self,outname="plots.tex",plotnames=[],varotra="",base=""):

     actualDir=os.path.abspath(".")
     elpath=actualDir
     self.title=""
     
     
    ####################################################
    # Genera el path base, donde estara el ps
    # 
     for actorig in self.parser_original.act:
      # self.title += ", %s=%s"%actorig
       if actorig[0] in self.parser_original.vars:
         elpath+="/%s-%s"%actorig
         try:
 	   if not os.path.exists(elpath):
 	     print "Error el path no existe",elpath
 	     raise TypeError, "Error"
 	 except:
 	    sys.exit()  
    #
    #
    #####################################################
     
     os.chdir(elpath)
     os.system("~/opt/bin/ctprint.sh")
     cout=sys.stdout
     sys.stdout=open(elpath+"/"+outname,"w")     

     
     print "\\documentclass[12pt]{article}"
     print 
     print "\\usepackage{graphicx}"
     print 
     print "\\begin{document}"
     print 
     print 
     print "Gr\\'aficos generados con los siguientes par\\'ametros:"
     print "\\begin{itemize}"
     for i in self.parser_original.act:
         print "\\item    { \\tt" ,
         if i[1] == '':
	   posunder=i[0].find("_")
	   if posunder>0:
	     posblank=i[0].find("0")
	     print "\\begin{verbatim}"
	     print i[0],
	     print "\\end{verbatim}"
	   else:
	     print i[0],
	 else:
	   print " $ %s = %s $" % i , 
	 print """ }   """  
     print "\\end{itemize}"
     print  
     print 
     ac_floats=0
     for i in plotnames:
       print "\\begin{figure}[!ht]"
       print "\\begin{center}"
       print "\\includegraphics[height=10cm,angle=-90]{%s%s.agr.eps}"%(base+str(i[0]),varotra)
       print "\\caption{Par\\'ametro $%s$ vs. $%s$}"%(agr2tex(i[1]),varotra)
       print "\\end{center}"
       print "\\end{figure}"
       ac_floats+=1
       if ac_floats % 12 == 0:
         print "\\clearpage"
       

     print "\\end{document}"
     sys.stdout=cout
     os.system("latex %s"%outname)
     comandoexec= "dvips -o ../%s.ps  %s"%(base+os.path.split(elpath)[-1], os.path.splitext(outname)[0]+".dvi")
     os.system(comandoexec)
     
     os.chdir(actualDir)

   def doit(self,outname="plots.tex",plotnames=[],varotra="",base=""):

     flag=1
  
     while flag:
      self.tex(outname,plotnames,varotra,base)
      flag=self.next()
     
     self.parser_original.reset()
   
