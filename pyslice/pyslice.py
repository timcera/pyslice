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
import sys, os, getopt, time, string
import os.path
import signal
import re
import ConfigParser
import shutil
import pyslice_lib.PySPG as pyspg

#===globals======================
modname="pyslice"
__version__="1.3"

#--option args--
debug_p = 0
#opt_b=None  #string arg, default is undefined

#---positional args, default is empty---
pargs = []    

#---other---

#===utilities====================
def msg(txt):
  sys.stdout.write(txt)
  sys.stdout.flush()

def debug(ftn, txt):
  if debug_p:
    tmp=string.join([modname,'.',ftn,':',txt,'\n'],'')
    sys.stdout.write(tmp)
    sys.stdout.flush()

def fatal(ftn, txt):
  tmp=string.join([modname,'.',ftn,':FATAL:',txt,'\n'],'')
  raise SystemExit, tmp
 
def usage():
  print __doc__

activeChildren = []

def mask(charlist):
  """
  Construct a mask suitable for string.translate,
  which marks letters in charlist as "t" and ones not as "b"
  """
  mask=""
  for i in range(256):
    if chr(i) in charlist: mask=mask+"t"
    else: mask=mask+"b"
  return mask

ascii7bit=string.joinfields(map(chr, range(32,127)), "")+"\r\n\t\b"
ascii7bit_mask=mask(ascii7bit)

def istext(filep, check=1024, mask=ascii7bit_mask):
  """
  Returns true if the first check characters in file
  are within mask, false otherwise
  """

  try:
    s=filep.read(check)
    filep.close()
    s=string.translate(s, mask)
    if string.find(s, "b") != -1: return 0
    return 1
  except (AttributeError, NameError): # Other exceptions?
    return istext(open(filep, "r"))


#====================================
class Pyslice:
  #---class variables---
  #--------------------------
  def __init__(self):
    #---instance variables---
    pass

  #--------------------------
  def read_config(self, min_sections, max_sections, req_sections_list):
    """ Reads the pyslice.conf file.

    """
    pyslice_conf = os.getcwd() + os.sep + "pyslice.conf"
    if not os.access(pyslice_conf, os.F_OK | os.R_OK):
      NotFound = "\n***\nThe pyslice.conf file was not found or not readable"
      raise NotFound,"\npyslice.conf must be in the current directory\n***\n"
    config_dict = ConfigParser.ConfigParser()
    config_dict.read(pyslice_conf)
    num_sections = len(config_dict.sections())
    if num_sections < min_sections or num_sections > max_sections:
      ConfigFile = "\n***\nThe pyslice.conf file has an incorrect number of sections"
      raise ConfigFile, "\npyslice.conf must have between %d and %d sections.\n***\n" % (min_sections, max_sections)
    for sec in req_sections_list:
      if not config_dict.has_section(sec):
        NoSection = "\n***\nThe pyslice.conf file is missing a required section"
        raise NoSection,"\npyslice.conf requires the [%s] section.\n***\n" % sec
    return config_dict

  def dequote(self, in_str):
    """ Removes quotes around strings in the configuration file.

    """
    in_str = string.replace(in_str, '\'', '')
    in_str = string.replace(in_str, '\"', '')
    return in_str

  def path_correction(self, path):
    """ Corrects path seperators and removes trailing path seperators.

    Needed so that path seperators of any OS are corrected to the
    platform running the script.

    """
    path = string.replace(path, "/", os.sep)
    path = string.replace(path, "\\", os.sep)
    if path[-1] == "/" or path[-1] == "\\":
      path = path[:-1]
    return path


  def daemonize(self, dir_slash='/', logto="/dev/null"):
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
    os.chdir(dir_slash)

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
    ftn = "Pyslice.run"
    debug(ftn,"hello, world")

    print "\n    Pyslice will replace all files in the output directories with the\n    same name as files in the template directory.  If this is not\n    what you want, move the files as necessary.  Pyslice also does\n    not check if the permutation schedule is the same and may not use\n    the same number of output directories from previous pyslice runs.\n" 
    raw_input('Press any key to continue . . .')
    print

    # Read the configuration file and set appropriate variables.
    configuration = self.read_config(4, 100, ["paths", "flags", "program"])
    template_path = self.dequote(configuration.get("paths", "template_path"))
    output_path = self.dequote(configuration.get("paths", "output_path"))
    keyword = self.dequote(configuration.get("flags", "keyword"))
    max_processes = configuration.getint("flags", "max_processes")
    flat_dirs = self.dequote(configuration.get("flags", "flat_dirs"))
    program = self.dequote(configuration.get("program", "program"))

    # Remove the standard configuration sections to leave all of the variables.
    section_list = configuration.sections()
    del section_list[section_list.index("paths")]
    del section_list[section_list.index("flags")]
    del section_list[section_list.index("program")]

    # Make sure to clean up the paths.
    template_path = self.path_correction(template_path)
    output_path = self.path_correction(output_path)

    # Put all variable names from configuration file into key_list.
    # Create list (from each variable) of lists (from start, stop, incr).
    list_list = []
    for variable in section_list:
      var_type = configuration.get(variable, "type")
      var_list = []
      if var_type == "arithmetic":
        var_list.append("+")
        var_list.append(variable)
      if var_type == "geometric":
        var_list.append("*")
        var_list.append(variable)
      if var_type == "arithmetic" or var_type == "geometric":
        var_list.append(configuration.getfloat(variable, "start"))
        var_list.append(configuration.getfloat(variable, "stop"))
        var_list.append(configuration.getfloat(variable, "increment"))
      if var_type == "list":
        var_list.append(".")
        var_list.append(variable)
        for i in range(1,1000):
          try:
            var_list.append(configuration.get(variable, "value%i" % (i)))
          except ConfigParser.NoOptionError:
            break
      var_list = [str(i) for i in var_list]
      list_list.append(var_list)

    list_list = [string.join(i) for i in list_list]

    pyspg_obj = pyspg.ParamParser(list_list)

    # There should be a way to get this from the PySPG library...
    flag = True
    length = 0
    set = []
    while flag:
      length = length + 1
      tmp = []
      # Had to add the 'limit=None' in order to get directories created
      # for the last variable.  Is this a bug in PySPG?
      tmp.append(pyspg_obj.directory_tree(limit=None))
      for i in pyspg_obj.actual_values():
        tmp.append(i)
      set.append(tmp)
      flag = pyspg_obj.next()

    while 1:
      inp =  raw_input('Current configuration results in %s permutations. Continue? (y/n) > ' % len(set))[0] 
      if inp == 'n' or inp == 'N':
        return
      if inp == 'y' or inp == 'Y':
        break

    # Comment the following command in order to debug
    self.daemonize(os.getcwd())

    for var_index,var_set in enumerate(set):
      # Create label for output directories
      if flat_dirs[0] == 'Y' or flat_dirs[0] == 'y':
        strtag = string.zfill(var_index,5)
      else:
        strtag = var_set[0]

      # Operate on each file in template directory 
      for files in os.listdir(template_path):

        # Not ready to deal with sub-directories yet...
        if os.path.isdir(files):
          continue

        # Should work out a more robust error check
        try:
          os.makedirs(output_path + os.sep + strtag)
        except OSError:
          pass

        outfilepath = os.path.abspath(output_path + os.sep + 
                                      strtag + os.sep + files)

        infilepath = os.path.abspath(template_path + os.sep + files)

        # Is this a binary file?  If so, just copy
        if istext(infilepath):
          inputf = open(infilepath,'r')
        else:
          shutil.copy(infilepath, outfilepath)
          continue
          
        output = open(outfilepath,'w')
        shutil.copystat(infilepath, outfilepath)

        # Search for keywordvarnamekeyword and replace with appropriate value.
        while 1:
          line = inputf.readline()
          if not line: 
            break
          for variables in var_set[1:]:
            var_name = variables[0]
            var_value = variables[1]
            # compile re search for keyword .* variable_name .* keyword
            search_for = re.compile(re.escape(keyword) + '(' + r'.*?' + var_name + r'.*?' + ')' + re.escape(keyword))
            # while there are still matchs available on the line
            while search_for.search(line):
              # only have 1 group, but it returns a 2 item tuple, need [0]
              match = search_for.search(line).groups()[0]
              # replace variable name with number
              match = string.replace(match, var_name, str(var_value))
              # evaluate Python statement with restricted eval
              match = eval(match)
              # replace variable with calculated value
              line = re.sub(search_for, str(match), line, count=1)
          # writes new line out to output file
          output.write(line)

        inputf.close()
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
          os.execvpe(command_args[0], command_args, os.environ)
        else:
          activeChildren.append(childPid)

#=============================
def main(args):
  main_x=Pyslice()
  main_x.run()
    
#-------------------------
if __name__ == '__main__':
  ftn = "main"
  opts, pargs = getopt.getopt(sys.argv[1:], 'hvd',
               ['help', 'version', 'debug', 'bb='])
  for opt in opts:
    if opt[0] == '-h' or opt[0] == '--help':
      print modname+": version="+__version__
      usage()
      sys.exit(0)
    elif opt[0] == '-v' or opt[0] == '--version':
      print modname+": version="+__version__
      sys.exit(0)
    elif opt[0] == '-d' or opt[0] == '--debug':
      debug_p = 1
    elif opt[0] == '--bb':
      opt_b = opt[1]

  #---make the object and run it---
  main(pargs)

