#!/usr/bin/env python
# pyslice.py 
#    Copyright (C) 2001  Tim Cera timcera@earthlink.net
#    http://home.earthlink.net/~timcera
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


"""
NAME:
    pyslice.py  

SYNOPSIS:
    pyslice.py [options] 

DESCRIPTION:
    Pyslice creates input data sets from information in pyslice.conf
    and files in the template directory.  Pyslice then runs a command
    within each directory, controlling the processes so that at any
    one time there are less than a certain number of processes.

OPTIONS:
    -h,--help        this message
    -v,--version     version
    -d,--debug       turn on debug messages

EXAMPLES:
    1. As standalone
        pyslice.py 
    2. As library
        import pyslice
        ...
"""
#===imports======================
import sys,os,getopt,time,string
import os.path
import signal
import re
import rexec
import UserList
import math

#===globals======================
modname="pyslice"
__version__="1.0"

#--option args--
debug_p=0
#opt_b=None  #string arg, default is undefined

#---positional args, default is empty---
pargs=[]    

#---other---

#===utilities====================
def msg(txt):
  sys.stdout.write(txt)
  sys.stdout.flush()

def debug(ftn,txt):
  if debug_p:
    tmp=string.join([modname,'.',ftn,':',txt,'\n'],'')
    sys.stdout.write(tmp)
    sys.stdout.flush()

def fatal(ftn,txt):
  tmp=string.join([modname,'.',ftn,':FATAL:',txt,'\n'],'')
  raise SystemExit, tmp
 
def usage():
  print __doc__

activeChildren = []


class frange(UserList.UserList):
  """
  frange(stop) # assume start=0, step=1
  frange(start, stop) # assume step=1
  frange(start, stop, step)
  returns a list of values from start up to stop, with step step.
  Unlike range(), stop value is included in the list, if it is equal
  to the last value of the arithmetic sequence.
  If the returned list is too big, you may want to use xfrange class.
  This class is not resistant to rounding errors, e.g. on my computer:

  >>> frange(0.7, 0, -0.1)
  [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
  >>> frange(0.7, -0.05, -0.1)
  [0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, -1.11022302463e-16]

  """

  def __init__(self, *args):
    l = len(args)
    if l == 1: # only to
      args.insert(0,0)
      args.append = 1
    elif l == 2: # from, to
      args.append = 1

    self.start, self.stop, self.step = args
    startstr = string.split(str(args[0]),'.')
    stopstr  = string.split(str(args[1]),'.')
    stepstr  = string.split(str(args[2]),'.')

    max_dec    = max(len(startstr[1]),
                     len(stopstr[1]),
                     len(stepstr[1]))
    mult = math.pow(10,max_dec)

    self.data = range(int(self.start*mult),
                      int(self.stop*mult),
                      int(self.step*mult))

    self.data = map(lambda x,mult=mult: x/mult, self.data)


  def __repr__(self):
    return "frange(%i, %i, %i)" % (self.start, self.stop, self.step)

  def __str__(self):
    return str(self.data)

  def __len__(self):
    return len(self.data)

#====================================
class Pyslice:
  #---class variables---
  #--------------------------
  def __init__(self):
    ftn="Pyslice.__init__"
    #---instance variables---
    (self.year,self.month,self.day,self.hour,self.minute,self.second,
     self.weekday,self.julianday,self.daylight)=time.localtime(time.time())
  #--------------------------
  def read_config(self,min_sections,max_sections,req_sections_list):
    """ Reads the pyslice.conf file.

    """
    from ConfigParser import *
    pyslice_conf = os.getcwd() + os.sep + "pyslice.conf"
    if not os.access(pyslice_conf,os.F_OK | os.R_OK):
      NotFound = "\n***\nThe pyslice.conf file was not found or not readable"
      raise NotFound,"\npyslice.conf must be in the current directory\n***\n"
    config_dict = ConfigParser()
    config_dict.read(pyslice_conf)
    num_sections = len(config_dict.sections())
    if num_sections < min_sections or num_sections > max_sections:
      ConfigFile = "\n***\nThe pyslice.conf file has an incorrect number of sections"
      raise ConfigFile,"\npyslice.conf must have between %d and %d sections.\n***\n" % (min_sections,max_sections)
    for sec in req_sections_list:
      if not config_dict.has_section(sec):
        NoSection = "\n***\nThe pyslice.conf file is missing a required section"
        raise NoSection,"\npyslice.conf requires the [%s] section.\n***\n" % sec
    return config_dict

  def dequote(self,str):
    """ Removes quotes around strings in the configuration file.

    """
    str = string.replace(str,'\'','')
    str = string.replace(str,'\"','')
    return str

  def path_correction(self,str):
    """ Corrects path seperators and removes trailing path seperators.

    Needed so that path seperators of any OS are corrected to the
    platform running the script.

    """
    str = string.replace(str,"/",os.sep)
    str = string.replace(str,"\\",os.sep)
    if str[-1] == "/" or str[-1] == "\\":
      str = str[:-1]
    return str

  def cartesian(self,listList):
    """ Determines the 'cartesian' of a list of lists.

    The cartesian is the permutation of all combinations _between_
    lists.  Got this nugget off of comp.lang.python posted by Bryan
    Olson.  Good thing too because there is no way I could have
    figured it out on my own.

    """
    if listList:
      result = []
      prod = self.cartesian(listList[:-1])
      for x in prod:
        for y in listList[-1]:
          result.append(x + (y,))
      return result
    return [()]      

  def daemonize(self,dir='/', logto="/dev/null"):
    """ Forces current process into the background.

    Got off the comp.lang.python newsgroup.  Written by Michael Romberg.

    """
    #
    # Close open files
    #
    sys.stdin.close()
    sys.stdout.close()
    sys.stderr.close()

    #
    # Change the cwd
    #
    os.chdir(dir)

    #
    # Background the process by forking and exiting the parent
    #
    if os.fork() != 0:
      # -- Parent --
      sys.exit()

    # -- Child --

    # redirect stdout and stderr to /dev/null
    #sys.stdin = open("/dev/null", "r")
    sys.stdout = open(logto, "wb", 0)
    sys.stderr = sys.stdout

    #
    # Set the umask
    #
    os.umask(0)

    #
    # Disassociate from Process Group
    #
    os.setpgrp()

    #
    # Ignore Terminal I/O Signals
    #
    if hasattr(signal, 'SIGTTOU'):
      signal.signal(signal.SIGTTOU, signal.SIG_IGN)
    if hasattr(signal, 'SIGTTIN'):
      signal.signal(signal.SIGTTIN, signal.SIG_IGN)
    if hasattr(signal, 'SIGTSTP'):
      signal.signal(signal.SIGTSTP, signal.SIG_IGN)

  def reapChildren(self):
    while activeChildren:
      pid,stat = os.waitpid(0,os.WNOHANG)
      if not pid:
        break
      activeChildren.remove(pid)

  def run(self):
    ftn="Pyslice.run"
    debug(ftn,"hello, world")

    print "\n    Pyslice will replace all files in the output directories with the\n    same name as files in the template directory.  If this is not\n    what you want, move the files as necessary.  Pyslice also does\n    not check if the permutation schedule is the same and may not use\n    the same number of output directories from previous pyslice runs.\n" 
    raw_input('Press any key to continue . . .')
    print

    # Read the configuration file and set appropriate variables.
    configuration = self.read_config(4,100,["paths","flags","program"])
    template_path = self.dequote(configuration.get("paths","template_path"))
    output_path = self.dequote(configuration.get("paths","output_path"))
    keyword = self.dequote(configuration.get("flags","keyword"))
    max_processes = configuration.getint("flags","max_processes")
    program = self.dequote(configuration.get("program","program"))

    # Remove the standard configuration sections to leave all of the variables.
    configuration.remove_section("paths")
    configuration.remove_section("flags")
    configuration.remove_section("program")

    # Make sure to clean up the paths.
    template_path = self.path_correction(template_path)
    output_path = self.path_correction(output_path)

    # Put all variable names from configuration file into key_list.
    # Create list (from each variable) of lists (from start, stop, incr).
    key_list = []
    list_list = []
    for variable in configuration.sections():
      start = configuration.getfloat(variable,"start")
      stop = configuration.getfloat(variable,"stop")
      incr = configuration.getfloat(variable,"increment")
      list_list.append(frange(start,stop,incr))
      key_list.append(variable)

    # Create cartesian (all combinations of input variables)
    set = self.cartesian(list_list)

    while 1:
      inp =  raw_input('Current configuration results in %s permutations. Continue? (y/n) > ' % len(set))[0] 
      if inp == 'n' or inp == 'N':
        return
      if inp == 'y' or inp == 'Y':
        break

    self.daemonize(os.getcwd())

    pid_list = []
    guard = rexec.RExec()
    for var_index in range(len(set)):
      # Create label for output directories
      strtag = string.zfill(var_index,5)
     
      # Operate on each file in template directory 
      for file in os.listdir(template_path):
        infilepath = os.path.abspath(template_path + os.sep + file)
        input = open(infilepath,'r')

        # Should work out a more robust error check
        try:
          os.makedirs(output_path + os.sep + strtag)
        except OSError:
          pass
        outfilepath = os.path.abspath(output_path + os.sep + 
                                      strtag + os.sep + file)
        output = open(outfilepath,'w')

        # Search for keywordvarnamekeyword and replace with appropriate value.
        while 1:
          line = input.readline()
          if not line: break
          for key_index in range(len(key_list)):
            # compile re search for keyword .* variable_name .* keyword
            search_for = re.compile(re.escape(keyword) + '(' + r'.*?' + key_list[key_index] + r'.*?' + ')' + re.escape(keyword))
            # while there are still matchs available on the line
            while re.search(search_for,line):
              # only have 1 group, but it returns a 2 item tuple, need [0]
              match = re.search(search_for,line).groups()[0]
              # replace variable name with number
              match = string.replace(match,key_list[key_index],str(set[var_index][key_index]))
              # evaluate Python statement with restricted eval
              match = guard.r_eval(match)
              # replace variable with calculated value
              line = re.sub(search_for,str(match),line,count=1)
          # writes new line out to output file
          output.write(line)

        input.close()
        output.close()

      if max_processes > 0:
        # Wait until there are less than max_processes.
        while len(activeChildren) >= max_processes:
          self.reapChildren()
          time.sleep(5)

        # use time.sleep to slightly stagger processes reading the command
        time.sleep(1)
        # Create new child and execute program.
        childPid = os.fork()
        if childPid == 0:
          os.chdir(output_path + os.sep + strtag)
          command_args = string.split(program)
          os.execvpe(command_args[0],command_args,os.environ)
        else:
          activeChildren.append(childPid)

#=============================
def main(args):
  x=Pyslice()
  x.run()
    
#-------------------------
if __name__ == '__main__':
  ftn = "main"
  opts,pargs=getopt.getopt(sys.argv[1:],'hvd',
             ['help','version','debug','bb='])
  for opt in opts:
    if opt[0]=='-h' or opt[0]=='--help':
      print modname+": version="+__version__
      usage()
      sys.exit(0)
    elif opt[0]=='-v' or opt[0]=='--version':
      print modname+": version="+__version__
      sys.exit(0)
    elif opt[0]=='-d' or opt[0]=='--debug':
      debug_p=1
    elif opt[0]=='--bb':
      opt_b=opt[1]

  #---make the object and run it---
  main(pargs)

