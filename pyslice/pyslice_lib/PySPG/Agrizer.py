#! /usr/bin/python
#
#
# :::~ Author: Claudio Juan Tessone <tessonec@imedea.uib.es> (c) 2002-2003
#
# Distributed According to GNU Generic Purpose License (GPL)
# Please visit www.gnu.org
################################################################################

######################################################################
######################################################################

class Agrizer(ParamParser):

   xcol=0
   ycol=1
   xformula="x"
   yformula="y"
   xlabel="x"
   ylabel="y"
   xscale="Normal"
   yscale="Normal"

   def agr(self,outname="out.agr",inname="out.dat"):

     title=""
     elpath=""
     ac_values=self.actual_values()
     for actual in ac_values:
       title += " %s=%s "%actual
       legend=" %s = %s "%actual

       if actual[0] in self.isvariable[:-1]:
         elpath+="%s-%s/"%actual

     try:
       if not os.path.exists(elpath):
         raise AssertError, ""
     except:
       print "Error accesing path: '%s'."%elpath
       sys.exit()

     os.chdir(elpath)

     sys.stdout = open (outname,"w")

     ls= load.loadXY(inname,self.xcol,self.ycol)
     ls2 = load.transformXY(ls,self.xformula,self.yformula)

     g1=pygrace.GraceDocument()
     g1.set_data(ls2,legend)

     g1.autoscale()
     g1.set_labels(self.xlabel,self.ylabel)
     g1.set_scale(self.xscale,self.yscale)
     g1.set_title(title)
     g1.dump()

     os.chdir(cwd)


   def doit(self,outname="out.agr",inname="out.dat"):
     flag=1#self.next()

     while flag:
      self.agr(outname,inname)
      flag=self.next()
     self.reset()


