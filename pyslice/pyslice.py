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
    Pyslice creates input data sets from information in pyslice.ini
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
import subprocess
import os.path
import re
import ConfigParser
import shutil
import pyslice_lib.PySPG as pyspg
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

# To support montecarlo...
import random

#===globals======================
modname = "pyslice"
__version__ = "1.6.5"


#--option args--
debug_p = 0

global input_file
input_file = "pyslice.ini"

#---positional args, default is empty---
pargs = []    

#---other---

# Didn't want to have an infinite amount of jobs.
# This is just for if user makes max_threads <= 0.
total_processes = 64


#===utilities====================
def msg(txt):
    sys.stdout.write(txt)
    sys.stdout.flush()

def debug(ftn, txt):
    if debug_p:
        tmp = string.join([modname, '.', ftn, ':', txt, '\n'], '')
        sys.stdout.write(tmp)
        sys.stdout.flush()

def fatal(ftn, txt):
    tmp = string.join([modname, '.', ftn, ':FATAL:', txt, '\n'], '')
    raise SystemExit, tmp
 
def usage():
    print __doc__


def mask(charlist):
    """
    Construct a mask suitable for string.translate,
    which marks letters in charlist as "t" and ones not as "b".
    Used by 'istext' function to identify text files.
    """
    mask = ""
    for i in range(256):
        if chr(i) in charlist: 
            mask = mask + "t"
        else: 
            mask = mask + "b"
    return mask

ascii7bit = string.joinfields(map(chr, range(32, 127)), "")+"\r\n\t\b"
ascii7bit_mask = mask(ascii7bit)

def istext(filep, check=1024, mask=ascii7bit_mask):
    """
    Returns true if the first check characters in file
    are within mask, false otherwise. 
    """

    try:
        s = filep.read(check)
        filep.close()
        s = string.translate(s, mask)
        if string.find(s, "b") != -1: 
            return 0
        return 1
    except (AttributeError, NameError): # Other exceptions?
        return istext(open(filep, "r"))


# User-defined Exceptions
class NumberConfigSectionsError(Exception):
    pass

class ConfigFileNotFoundError(Exception):
    pass

class RequiredSectionNotFoundError(Exception):
    pass
        
class NotValidTypeError(Exception):
    pass

class TemplatePathNotFoundError(Exception):
    pass

#====================================
class Pyslice:
    #---class variables---
    #--------------------------
    def __init__(self):
        #---instance variables---
        pass

    #--------------------------
    def read_config(self, min_sections, max_sections, req_sections_list):
        """ Reads the pyslice.ini file.
  
        """
  
        # Can we find pyslice.ini?
        pyslice_ini = os.path.join(os.getcwd(), input_file)
        if not os.access(pyslice_ini, os.F_OK | os.R_OK):
            raise ConfigFileNotFound("%s was not found or not readable ***" % (input_file,))
  
        # Read it in.
        config_dict = ConfigParser.ConfigParser()
        config_dict.read(pyslice_ini)
  
        # Is pyslice.ini minimally error free?
        num_sections = len(config_dict.sections())
        if num_sections < min_sections or num_sections > max_sections:
            raise NumberConfigSectionsError("pyslice.ini must have between %d and %d sections." % (min_sections, max_sections))
        for sec in req_sections_list:
            if not config_dict.has_section(sec):
                raise RequiredSectionNotFoundError("pyslice.ini requires the [%s] section." % sec)
    
        # Return pyslice.ini as dictionary.
        return config_dict


    def dequote(self, in_str):
        """ Removes quotes around strings in the configuration file.
            This corrects a mistake that I would commonly make.
  
        """
        in_str = string.replace(in_str, '\'', '')
        in_str = string.replace(in_str, '\"', '')
        return in_str
  

    def path_correction(self, path):
        """ Corrects path separators and removes trailing path separators.
  
        Needed so that path separators of any OS are corrected to the
        platform running the script.
  
        """
        path = string.replace(path, "/", os.sep)
        path = string.replace(path, "\\", os.sep)
        if path[-1] == "/" or path[-1] == "\\":
            path = path[:-1] 
        return path

    def create_output(self, var_set, dirname, fnames):
        try:
            os.makedirs(os.path.join(_output_path, _strtag))
        except OSError:
            pass
        for files in fnames:
            infilepath = os.path.join(dirname, files)
            rel_dir = infilepath.replace(_template_path + os.sep, '')
            outfilepath = os.path.join(_output_path, _strtag, rel_dir)
  
            # Sub-directories in template directory
            if os.path.isdir(infilepath):
                try:
                    os.makedirs(outfilepath)
                    continue
                except OSError:
                    continue
  
            # Is this a text file?  If so, just open as a template
            if istext(infilepath):
                inputf = open(infilepath, 'r')
            else:
                shutil.copy(infilepath, outfilepath)
                continue
  
            output = open(outfilepath,'w')
            shutil.copystat(infilepath, outfilepath)
  
            # Search for _keywordvarname_keyword and replace with appropriate
            # value.
            for line in inputf:
                for variables in var_set[1:]:
                    var_name = variables[0]
                    var_value = variables[1]
                    # compile re search for _keyword .* variable_name .*
                    # _keyword
                    search_for = re.compile(
                        re.escape(_keyword) + '(' + r'.*?' + 
                        var_name + r'.*?' + ')' + re.escape(_keyword))
                    # while there are still matchs available on the line
                    while search_for.search(line):
                        # only have 1 group, but it returns a 2 item tuple,
                        # need [0]
                        match = search_for.search(line).groups()[0]
                        # replace variable name with number
                        match = string.replace(match, var_name, str(var_value))
                        # evaluate Python statement with eval
                        match = eval(match)
                        # replace variable with calculated value
                        line = re.sub(search_for, str(match), line, count=1)
                # writes new line out to output file
                output.write(line)
  
            inputf.close()
            output.close()

    # Runs the command *com in a new thread.
    def start_thread_process(self, *com):
        com = string.join(com, ' ')
        if os.name != 'nt':
            p = subprocess.Popen(com, shell=True, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        else:
            # close_fds is not supported on Windows
            p = subprocess.Popen(com, shell=True, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        (chstdin, chstdouterr) = (p.stdin, p.stdout)

        fo = open('pyslice.log', 'w')
        fo.write(string.join(chstdouterr.readlines()))
        fo.close()

    def run(self):
        global _strtag
        global _output_path
        global _keyword
        global _template_path

        ftn = "Pyslice.run"
        debug(ftn,"hello, world")

        raw_input("""
        Pyslice will replace all files in the output directories with the same
        name as files in the template directory.  If this is not what you want,
        move the files as necessary.  Pyslice also does not check if the
        permutation schedule is the same and may not use the same number of
        output directories from previous pyslice runs. 

        'Press any key to continue . . .'
                  """)

        # Read the configuration file and set appropriate variables.
        configuration = self.read_config(4, 100, ["paths", "flags", "program"])
        _template_path = self.dequote(configuration.get("paths", 
                                                        "template_path"))
        _output_path = self.dequote(configuration.get("paths", "output_path"))
        _keyword = self.dequote(configuration.get("flags", "keyword"))
        max_threads = configuration.getint("flags", "max_threads")
        if max_threads <= 0:
            max_threads = total_processes
        flat_dirs = configuration.getboolean("flags", "flat_dirs")
        program = self.dequote(configuration.get("program", "program"))

        # Remove the standard configuration sections to leave all of the
        # variables.
        section_list = configuration.sections()
        del section_list[section_list.index("paths")]
        del section_list[section_list.index("flags")]
        del section_list[section_list.index("program")]

        # Make sure to clean up the paths.
        _template_path = os.path.abspath(self.path_correction(_template_path))
        _output_path = os.path.abspath(self.path_correction(_output_path))

        if not os.path.exists(_template_path):
            raise TemplatePathNotFoundError("The template path doesn't exists at '%s'" % (_template_path))

        # Put all variable names from configuration file into key_list.
        # Create list (from each variable) of lists (from start, stop, incr).
        list_list = []
        for variable in section_list:
            var_type = configuration.get(variable, "type")
            var_list = []

            # Monte Carlo
            if var_type == "montecarlo":
                # Cheat by using list type
                var_list.append(".%s" % (variable,))
                # Find out distribution
                distribution = 'random.' + configuration.get(variable, 
                                                             "distribution")
                samples = configuration.getint(variable, "samples")
                for samp in range(samples):
                    var_list.append(eval(distribution))
            # Arithmetic
            elif var_type == "arithmetic":
                var_list.append("+%s" % (variable,))
            # Geometric
            elif var_type == "geometric":
                var_list.append("*%s" % (variable,))
            # List
            elif var_type == "list":
                var_list.append(".%s" % (variable,))
                for i in eval(configuration.get(variable, "values_list")):
                    var_list.append(i)
            else:
                raise NotValidTypeError("'%s' is not a valid type - ['arithmetic', 'geometric', 'list', or 'montecarlo']" % (var_type,))

            # Arithmetic and Geometric types have the same variables
            if var_type == "arithmetic" or var_type == "geometric":
                var_list.append(configuration.getfloat(variable, "start"))
                var_list.append(configuration.getfloat(variable, "stop"))
                var_list.append(configuration.getfloat(variable, "increment"))

            var_list = [str(i) for i in var_list]
            list_list.append(var_list)

        list_list = [string.join(i) for i in list_list]

        # This does the cartesian of all of the parameter values.
        pyspg_obj = pyspg.ParamParser(list_list)

        # set will contain ['directory', [var, var_value], [var1, var1_value],
        # ...]
        set = []
        # Loop reorganizes the output from PySPG and retrieves the actual
        # values.

        for iter in pyspg_obj:
            tmp = []
            # Had to add the 'limit=None' in order to get directories created
            # for the last variable.  Is this a bug in PySPG?
            tmp.append(pyspg_obj.directory_tree(limit=None))
            for i in pyspg_obj.actual_values.items():
                tmp.append(i)
            set.append(tmp)

        while 1:
            inp =  raw_input(
                '''Configuration results in %s permutations. Continue? (y/n) > ''' 
                % (len(set),)
                )
            if not inp:
                continue
            inp = inp[0]
            if inp == 'y' or inp == 'Y':
                break
            if inp == 'n' or inp == 'N':
                return
            continue

        for var_index, var_set in enumerate(set):
            # Create label for output directories
            if flat_dirs:
                _strtag = str(var_index).zfill(5)
            else:
                _strtag = var_set[0]

            # Create the files and directories from the template
            # Walks the _template_path directory structure
            os.path.walk(_template_path, self.create_output, var_set)


            # Wait until there are less than max_threads.
            while _threading.activeCount() > max_threads:
                time.sleep(0.01)

            abs_path = os.path.join(_output_path, _strtag)

            os.chdir(abs_path)

            a = _threading.Thread(target=self.start_thread_process, 
                                  args=(program,))
            a.start()


#=============================
def main(option_dict):
    main_x = Pyslice()
    main_x.run()
      
#-------------------------
if __name__ == '__main__':
    ftn = "main"

    option_dict = {
                   'debug':0,
                   'file':'',
                  }
    opts, pargs = getopt.getopt(sys.argv[1:], 'hvdf:',
                 ['help', 'version', 'debug', 'file='])
    for opt in opts:
        if opt[0] == '-h' or opt[0] == '--help':
            print modname+": version="+__version__
            usage()
            sys.exit(0)
        elif opt[0] == '-v' or opt[0] == '--version':
            print modname+": version="+__version__
            sys.exit(0)
        elif opt[0] == '-d' or opt[0] == '--debug':
            option_dict['debug'] = 1
            sys.argv.remove(opt[0])
        elif opt[0] == '-f' or opt[0] == '--file':
            option_dict['file'] = opt[1]
            input_file = opt[1]
            sys.argv.remove(opt[0])
            sys.argv.remove(opt[1])

    #---make the object and run it---
    main(option_dict)

