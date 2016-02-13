#!/usr/bin/env python

from __future__ import print_function
from __future__ import absolute_import
from six.moves import map
from six.moves import range
from six.moves import input

# pyslice.py
#    Copyright (C) 2001  Tim Cera tim@cerazone.net
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name pyslice nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

# ===imports======================
import sys
import os
import getopt
import time
import subprocess
import os.path
import re
import shlex
import six.moves.configparser as configparser
import shutil
import filecmp
import math
# To support montecarlo...
import random

try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

from pyslice.pyslice_lib import PySPG as pyspg

# 2/3 compatibility
try:
    input = raw_input
except NameError:
    pass

# ===globals======================
modname = "pyslice"
__version__ = "1.6.5"
LINEENDS = '\r\n'


# --option args--
debug_p = 0

global input_file
input_file = "pyslice.ini"

# ---positional args, default is empty---
pargs = []

# ---other---

# Didn't want to have an infinite amount of jobs.
# This is just for if user makes max_threads <= 0.
total_processes = 64
numargs = 2
speciallines = {}

# ===utilities====================


def msg(txt):
    sys.stdout.write(txt)
    sys.stdout.flush()


def debug(ftn, txt):
    if debug_p:
        tmp = "".join([modname, '.', ftn, ':', txt, '\n'])
        sys.stdout.write(tmp)
        sys.stdout.flush()


def fatal(ftn, txt):
    tmp = "".join([modname, '.', ftn, ':FATAL:', txt, '\n'])
    raise SystemExit(tmp)


def usage():
    print(__doc__)


def mask(charlist):
    """
    Construct a mask suitable for s.translate,
    which marks letters in charlist as "t" and ones not as "b".
    Used by 'istext' function to identify text files.
    """
    maskvar = ""
    for i in range(256):
        if chr(i) in charlist:
            maskvar = maskvar + "t"
        else:
            maskvar = maskvar + "b"
    return maskvar

ascii7bit = "".join(
    list(map(chr, list(range(32, 127))))) + "\r\n\t\b"
ascii7bit_mask = mask(ascii7bit)


def istext(filename, check=1024, mask=ascii7bit_mask):
    """
    Returns true if the first check characters in file
    are within mask, false otherwise.
    """
    with open(filename, 'r') as filep:
        s = filep.read(check)
    s = s.translate(mask)
    if s.find("b") != -1:
        return 0
    return 1


def assignment(var1, var2):
    try:
        return var1
    except:
        return var2

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

# ====================================


class Pyslice:
    # ---class variables---
    # --------------------------

    def __init__(self):
        # ---instance variables---
        pass

    # --------------------------
    def read_config(self, min_sections, max_sections, req_sections_list):
        """ Reads the pyslice.ini file.

        """

        # Can we find pyslice.ini?
        pyslice_ini = os.path.join(os.getcwd(), input_file)
        if not os.access(pyslice_ini, os.F_OK | os.R_OK):
            raise ConfigFileNotFoundError(
                "%s was not found or not readable ***" % (input_file,))
        # Read it in.
        config_dict = configparser.ConfigParser()
        config_dict.read(pyslice_ini)

        # Is pyslice.ini minimally error free?
        num_sections = len(config_dict.sections())
        if num_sections < min_sections or num_sections > max_sections:
            raise NumberConfigSectionsError(
                "pyslice.ini must have between %d and %d sections." %
                (min_sections, max_sections))
        for sec in req_sections_list:
            if not config_dict.has_section(sec):
                raise RequiredSectionNotFoundError(
                    "pyslice.ini requires the [%s] section." % sec)

        # Return pyslice.ini as dictionary.
        return config_dict

    def dequote(self, in_str):
        """ Removes quotes around strings in the configuration file.
            This corrects a mistake that I would commonly make.

        """
        in_str = in_str.replace('\'', '')
        in_str = in_str.replace('\"', '')
        return in_str

    def path_correction(self, path):
        """ Corrects path separators and removes trailing path separators.

        Needed so that path separators of any OS are corrected to the
        platform running the script.

        """
        path = path.replace("/", os.sep)
        path = path.replace("\\", os.sep)
        if path[-1] == "/" or path[-1] == "\\":
            path = path[:-1]
        return path

    def create_output(self, var_set, dirname, dirs, fnames):
        var_dict = {}
        for variables in var_set[1:]:
            exec('%s = %s' % (variables[0], variables[1]))
            var_dict[variables[0]] = variables[1]

        try:
            os.makedirs(os.path.join(_output_path, _strtag))
        except OSError:
            pass
        for dirn in dirs:
            infilepath = os.path.join(dirname, dirn)
            rel_dir = infilepath.replace(_template_path + os.sep, '')
            try:
                os.makedirs(os.path.join(_output_path, _strtag, rel_dir))
            except OSError:
                pass
        for files in fnames:
            excludeflag = False
            for extensions in _exclude_list:
                if extensions in files:
                    excludeflag = True
            if excludeflag:
                continue
            infilepath = os.path.join(dirname, files)
            rel_dir = infilepath.replace(_template_path + os.sep, '')
            outfilepath = os.path.join(_output_path, _strtag, rel_dir)

            # Is this a text file?  If so, just open as a template
            if istext(infilepath):
                with open(infilepath, 'r') as inputf:
                    with open(outfilepath, 'w') as output:
                        shutil.copystat(infilepath, outfilepath)

                        filetotalizer = []
                        # Search for _keywordvarname_keyword and replace with
                        # appropriate value.
                        escaped_keyword = re.escape(_keyword)
                        keyword_search = re.compile(escaped_keyword)
                        search_for = re.compile(
                            escaped_keyword + '(.*?)' + escaped_keyword)

                        for lineraw in inputf:
                            line = lineraw
                            # Active comments first...
                            if CODE == line[:len(CODE)]:
                                filetotalizer.append(line)
                                words = line.split('|')
                                # There is the possibility that a datafile
                                # would WANT to use | So fix words up to have
                                # 1 or two items...

                                # if block length is missing... too cold
                                if len(words) == 1:
                                    linetemplate = words[0]
                                    blocklen = 1

                                # if template includes | ... too hot
                                # right now MUST include block length
                                if len(words) > numargs:
                                    linetemplate = words[:-2].join('|')
                                    blocklen = int(words[-1])

                                # ... just right
                                if len(words) == 2:
                                    linetemplate = words[0]
                                    blocklen = int(words[1])

                                linetemplate = linetemplate[len(CODE):]

                                # Process special directives
                                if '~' == linetemplate[1]:
                                    # Only want to open file once by checking
                                    # dictionary
                                    lookupno, filename = words[0].split()[1:3]
                                    lookupno = lookupno.split('~')[1]
                                    try:
                                        speciallines[filename]
                                    except KeyError:
                                        speciallines.setdefault(filename, {})
                                        for linespecial in open(filename, 'r'):
                                            # Handle comments and blank lines
                                            if '#' == linespecial[0]:
                                                continue
                                            recno, sep, stemplate = linespecial.partition(
                                                '|')
                                            if not stemplate:
                                                continue
                                            stemplate = stemplate.rstrip(LINEENDS)
                                            speciallines[filename][recno] = stemplate
                                    line_sub = speciallines[filename][
                                        lookupno].format(**var_dict)

                                else:
                                    line_sub = linetemplate.format(**var_dict)

                                for blockline in range(blocklen):
                                    linein = next(inputf)
                                    nline = []
                                    for index, char in enumerate(line_sub):
                                        if char == '*':
                                            nline.append(linein[index])
                                        else:
                                            nline.append(line_sub[index])
                                    filetotalizer.append(''.join(nline))
                            elif keyword_search.search(line):
                                matchline = line
                                for matches in search_for.findall(matchline):
                                    for var_name in var_dict:
                                        if var_name in matches:
                                            # replace variable name with number
                                            match = matches.replace(
                                                var_name, str(var_dict[var_name]))
                                            # evaluate Python statement with
                                            # eval
                                            match = eval(match)
                                            # replace variable with calculated
                                            # value
                                            matchwhat = re.escape(
                                                _keyword + matches + _keyword)
                                            matchline = re.sub(
                                                matchwhat, str(match), matchline, count=1)
                                filetotalizer.append(matchline)
                            else:
                                filetotalizer.append(line)
                        output.write(''.join(filetotalizer))
            else:
                try:
                    equalfiles = filecmp.cmp(infilepath, outfilepath)
                except OSError:
                    shutil.copy(infilepath, outfilepath)
                continue

    # Runs the command *com in a new thread.
    def start_thread_process(self, *com):
        com = ' '.join(com)
        com = shlex.split(com)
        # PYSLICE can be used in subprocess to do different things if script
        # is run outside of Pyslice.
        os.environ['PYSLICE'] = '1'
        if os.name != 'nt':
            p = subprocess.Popen(com,
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 close_fds=True)
        else:
            # close_fds is not supported on Windows
            p = subprocess.Popen(com,
                                 shell=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)

        (chstdin, chstdouterr) = (p.stdin, p.stdout)

        if _keep_log is True:
            with open('pyslice.log', 'w') as fo:
                fo.write(' '.join(str(i) for i in chstdouterr.readlines()))


    def run(self):
        global _strtag
        global _output_path
        global _keyword
        global _template_path
        global _exclude_list
        global _keep_log
        global CODE

        ftn = "Pyslice.run"
        debug(ftn, "hello, world")

        if len(sys.argv) == 1:

            toss = """
            Pyslice will replace all files in the output directories
            with the same name as files in the template directory.  If
            this is not what you want, move the files as necessary.  Pyslice
            also does not check if the permutation schedule is the same and
            may not use the same number of output directories from previous
            pyslice runs.

            'Press any key to continue . . .' """
            try:
                toss_again = input(toss)
            except NameError:
                toss_again = eval(input(toss))

        # Read the configuration file and set appropriate variables.
        configuration = self.read_config(4, 100, ["paths", "flags", "program"])
        _template_path = self.dequote(configuration.get("paths",
                                                        "template_path"))
        _output_path = self.dequote(configuration.get("paths", "output_path"))
        _keyword = self.dequote(configuration.get("flags", "keyword"))
        max_threads = configuration.getint("flags", "max_threads")
        try:
            COMMENT_CODE = configuration.get('flags', 'comment')
        except:
            COMMENT_CODE = 'qwerty'
        try:
            DT_CODE = assignment(
                configuration.get('flags', 'active_comment'), '')
        except:
            DT_CODE = 'qwerty'
        CODE = COMMENT_CODE + DT_CODE
        _exclude_list = []
        if configuration.has_option('flags', 'exclude_copy'):
            _exclude_list = eval(configuration.get('flags', 'exclude_copy'))
        if max_threads <= 0:
            max_threads = total_processes
        flat_dirs = configuration.getboolean("flags", "flat_dirs")
        try:
            _keep_log = configuration.getboolean("flags", "keep_log")
        except:
            _keep_log = True

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
            raise TemplatePathNotFoundError(
                "The template path doesn't exists at '%s'" % (_template_path))

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
                raise NotValidTypeError(
                    "'%s' is not a valid type - ['arithmetic', 'geometric', 'list', or 'montecarlo']" % (var_type,))

            # Arithmetic and Geometric types have the same variables
            if var_type == "arithmetic" or var_type == "geometric":
                start = configuration.getfloat(variable, "start")
                stop = configuration.getfloat(variable, "stop")
                increment = configuration.getfloat(variable, "increment")

                for i in [start, stop, increment]:
                    tmpi = i
                    if i == math.floor(i):
                        tmpi = int(i)
                    var_list.append(tmpi)

            var_list = [str(i) for i in var_list]
            list_list.append(var_list)

        list_list = [' '.join(i) for i in list_list]

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
            for i in list(pyspg_obj.actual_values.items()):
                tmp.append(i)
            set.append(tmp)

        while 1:
            try:
                if sys.argv[1] == 'y':
                    break
            except IndexError:
                pass

            toss = '''Configuration results in %s permutations. Continue? (y/n) > ''' % (len(set),)
            try:
                inp = input(toss)
            except NameError:
                inp = eval(input(toss))
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
            # os.path.walk(_template_path, self.create_output, var_set)
            for root, dirs, files in os.walk(_template_path):
                self.create_output(var_set, root, dirs, files)

            # Wait until there are less than max_threads.
            while _threading.activeCount() > max_threads:
                time.sleep(0.01)

            abs_path = os.path.join(_output_path, _strtag)

            os.chdir(abs_path)

            a = _threading.Thread(target=self.start_thread_process,
                                  args=(program,))
            a.start()


# =============================
class Usage(Exception):

    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv

    ftn = "main"

    option_dict = {
        'debug': 0,
        'file': '',
    }
    try:
        opts, pargs = getopt.getopt(argv[1:], 'hvdf:',
                                    ['help', 'version', 'debug', 'file='])
    except getopt.error as msg:
        raise Usage(msg)

    for opt in opts:
        if opt[0] == '-h' or opt[0] == '--help':
            print(modname + ": version=" + __version__)
            usage()
            sys.exit(0)
        elif opt[0] == '-v' or opt[0] == '--version':
            print(modname + ": version=" + __version__)
            sys.exit(0)
        elif opt[0] == '-d' or opt[0] == '--debug':
            option_dict['debug'] = 1
            sys.argv.remove(opt[0])
        elif opt[0] == '-f' or opt[0] == '--file':
            option_dict['file'] = opt[1]
            input_file = opt[1]
            argv.remove(opt[0])
            argv.remove(opt[1])

    # ---make the object and run it---
    main_x = Pyslice()
    main_x.run()

if __name__ == '__main__':
    sys.exit(main())
