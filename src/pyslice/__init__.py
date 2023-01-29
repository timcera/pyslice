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

import configparser
import filecmp
import getopt
import math
import os
import random  # has the appearance of not being used, but used in eval(...)
import re
import shlex
import shutil
import subprocess

# ===imports======================
import sys
import time
from contextlib import suppress
from pathlib import Path

from binaryornot.check import is_binary

try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

from pyslice.pyslice_lib import PySPG as pyspg

# ===globals======================
modname = "pyslice"
__version__ = "1.6.5"
LINEENDS = "\r\n"


# --option args--
debug_p = 0

global input_file
input_file = "pyslice.ini"

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
        tmp = "".join([modname, ".", ftn, ":", txt, "\n"])
        sys.stdout.write(tmp)
        sys.stdout.flush()


def fatal(ftn, txt):
    tmp = "".join([modname, ".", ftn, ":FATAL:", txt, "\n"])
    raise SystemExit(tmp)


def usage():
    print(__doc__)


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
        """Reads the pyslice.ini file."""

        # Can we find pyslice.ini?
        pyslice_ini = Path.cwd() / input_file
        if not os.access(pyslice_ini, os.F_OK | os.R_OK):
            raise ConfigFileNotFoundError(
                f"{input_file} was not found or not readable ***"
            )
        # Read it in.
        config_dict = configparser.ConfigParser()
        config_dict.read(pyslice_ini)

        # Is pyslice.ini minimally error free?
        num_sections = len(config_dict.sections())
        if num_sections < min_sections or num_sections > max_sections:
            raise NumberConfigSectionsError(
                f"pyslice.ini must have between {min_sections} and {max_sections} sections."
            )
        for sec in req_sections_list:
            if not config_dict.has_section(sec):
                raise RequiredSectionNotFoundError(
                    f"pyslice.ini requires the [{sec}] section."
                )

        # Return pyslice.ini as dictionary.
        return config_dict

    def dequote(self, in_str):
        """Removes quotes around strings in the configuration file.
        This corrects a mistake that I would commonly make.

        """
        in_str = in_str.replace("'", "")
        in_str = in_str.replace('"', "")
        return in_str

    def create_output(self, var_set, dirname, dirs, fnames):
        var_dict = {}
        for variables in var_set[1:]:
            exec(f"{variables[0]} = {variables[1]}")
            var_dict[variables[0]] = variables[1]

        with suppress(OSError):
            (Path(_output_path) / _strtag).mkdir(parents=True)
        for dirn in dirs:
            infilepath = Path(dirname) / dirn
            rel_dir = infilepath.relative_to(_template_path)
            with suppress(OSError):
                (Path(_output_path) / _strtag / rel_dir).mkdir()
        for files in fnames:
            excludeflag = False
            for extensions in _exclude_list:
                if extensions in files:
                    excludeflag = True
            if excludeflag:
                continue
            infilepath = Path(dirname) / files
            rel_dir = infilepath.relative_to(_template_path)
            outfilepath = Path(_output_path) / _strtag / rel_dir

            # Is this a text file?  If so, just open as a template
            if not is_binary(str(infilepath)):
                with open(infilepath) as inputf, open(outfilepath, "w") as output:
                    shutil.copystat(infilepath, outfilepath)

                    filetotalizer = []
                    # Search for _keywordvarname_keyword and replace with
                    # appropriate value.
                    escaped_keyword = re.escape(_keyword)
                    keyword_search = re.compile(escaped_keyword)
                    search_for = re.compile(f"{escaped_keyword}(.*?){escaped_keyword}")

                    for lineraw in inputf:
                        line = lineraw
                        # Active comments first...
                        if CODE == line[: len(CODE)]:
                            filetotalizer.append(line)
                            words = line.split("|")
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
                                linetemplate = words[:-2].join("|")
                                blocklen = int(words[-1])

                            # ... just right
                            if len(words) == 2:
                                linetemplate = words[0]
                                blocklen = int(words[1])

                            linetemplate = linetemplate[len(CODE) :]

                            # Process special directives
                            if linetemplate[1] == "~":
                                # Only want to open file once by checking
                                # dictionary
                                lookupno, filename = words[0].split()[1:3]
                                lookupno = lookupno.split("~")[1]
                                try:
                                    speciallines[filename]
                                except KeyError:
                                    speciallines.setdefault(filename, {})
                                    with open(filename) as lout:
                                        for line in lout:
                                            # Handle comments and blank lines
                                            if line[0] == "#":
                                                continue
                                            (
                                                recno,
                                                _,
                                                stemplate,
                                            ) = line.partition("|")
                                            if not stemplate:
                                                continue
                                            stemplate = stemplate.rstrip(LINEENDS)
                                            speciallines[filename][recno] = stemplate
                                line_sub = speciallines[filename][lookupno].format(
                                    **var_dict
                                )

                            else:
                                line_sub = linetemplate.format(**var_dict)

                            for _ in range(blocklen):
                                linein = next(inputf)
                                nline = []
                                for index, char in enumerate(line_sub):
                                    if char == "*":
                                        nline.append(linein[index])
                                    else:
                                        nline.append(line_sub[index])
                                nline.append(inputf.newlines)
                                filetotalizer.append("".join(nline))
                        elif keyword_search.search(line):
                            matchline = line
                            for matches in search_for.findall(matchline):
                                for key, var in var_dict.items():
                                    if key in matches:
                                        # replace variable name with number
                                        match = matches.replace(key, str(var))
                                        # evaluate Python statement with
                                        # eval
                                        match = eval(match)
                                        # replace variable with calculated
                                        # value
                                        matchwhat = re.escape(
                                            _keyword + matches + _keyword
                                        )
                                        matchline = re.sub(
                                            matchwhat,
                                            str(match),
                                            matchline,
                                            count=1,
                                        )
                            filetotalizer.append(matchline)
                        else:
                            filetotalizer.append(line)
                    output.write("".join(filetotalizer))
            else:
                try:
                    if filecmp.cmp(infilepath, outfilepath) is False:
                        shutil.copy(infilepath, outfilepath)
                except OSError:
                    shutil.copy(infilepath, outfilepath)
                continue

    # Runs the command *com in a new thread.
    def start_thread_process(self, *com):
        com = " ".join(com)
        com = shlex.split(com)
        # PYSLICE can be used in subprocess to do different things if script
        # is run outside of Pyslice.
        os.environ["PYSLICE"] = "1"
        if os.name != "nt":
            pype = subprocess.Popen(
                com,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True,
            )
        else:
            # close_fds is not supported on Windows
            pype = subprocess.Popen(
                com,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

        chstdouterr = pype.communicate()[0]

        if _keep_log is True:
            with open("pyslice.log", "w", encoding="utf8") as fpo:
                fpo.write(str(chstdouterr))

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

            'Press "Enter" to continue . . .' """
            _ = input(toss)

        # Read the configuration file and set appropriate variables.
        configuration = self.read_config(4, 100, ["paths", "flags", "program"])
        _template_path = self.dequote(configuration.get("paths", "template_path"))
        _output_path = self.dequote(configuration.get("paths", "output_path"))
        _keyword = self.dequote(configuration.get("flags", "keyword"))
        max_threads = configuration.getint("flags", "max_threads")
        try:
            comment_code = configuration.get("flags", "comment")
        except:
            comment_code = "qwerty"
        try:
            dt_code = assignment(configuration.get("flags", "active_comment"), "")
        except:
            dt_code = "qwerty"
        CODE = comment_code + dt_code
        _exclude_list = []
        if configuration.has_option("flags", "exclude_copy"):
            _exclude_list = eval(configuration.get("flags", "exclude_copy"))
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
        _template_path = Path.resolve(Path.cwd() / Path(_template_path))
        _output_path = Path.resolve(Path.cwd() / Path(_output_path))

        if not _template_path.exists():
            raise TemplatePathNotFoundError(
                f"The template path doesn't exists at '{_template_path}'"
            )

        # Put all variable names from configuration file into key_list.
        # Create list (from each variable) of lists (from start, stop, incr).
        list_list = []
        for variable in section_list:
            var_type = configuration.get(variable, "type")
            var_list = []

            # Monte Carlo
            if var_type == "montecarlo":
                # Cheat by using list type
                var_list.append(f".{variable}")
                # Find out distribution
                distribution = f"random.{configuration.get(variable, 'distribution')}"
                samples = configuration.getint(variable, "samples")
                for _ in range(samples):
                    var_list.append(eval(distribution))
            # Arithmetic
            elif var_type == "arithmetic":
                var_list.append(f"+{variable}")
            # Geometric
            elif var_type == "geometric":
                var_list.append(f"*{variable}")
            # List
            elif var_type == "list":
                var_list.append(f".{variable}")
                for i in eval(configuration.get(variable, "values_list")):
                    var_list.append(i)
            else:
                raise NotValidTypeError(
                    f"'{var_type}' is not a valid type - ['arithmetic', 'geometric', 'list', or 'montecarlo']"
                )

            # Arithmetic and Geometric types have the same variables
            if var_type in ("arithmetic", "geometric"):
                start = configuration.getfloat(variable, "start")
                stop = configuration.getfloat(variable, "stop")
                increment = configuration.getfloat(variable, "increment")

                for i in (start, stop, increment):
                    tmpi = i
                    if i == math.floor(i):
                        tmpi = int(i)
                    var_list.append(tmpi)

            var_list = [str(i) for i in var_list]
            list_list.append(var_list)

        list_list = [" ".join(i) for i in list_list]

        # This does the cartesian of all of the parameter values.
        pyspg_obj = pyspg.ParamParser(list_list)

        # nset will contain ['directory', [var, var_value], [var1, var1_value],
        # ...]
        nset = []
        # Loop reorganizes the output from PySPG and retrieves the actual
        # values.

        nmax = {}
        allints = {}
        for _ in pyspg_obj:
            tmp = []
            # Had to add the 'limit=None' in order to get directories created
            # for the last variable.  Is this a bug in PySPG?
            tmp.append(pyspg_obj.directory_tree(limit=None))

            for i_iter in pyspg_obj.variables_list:
                vname = i_iter.get_varname()
                nval = pyspg_obj.actual_values[vname]
                try:
                    nval = int(nval)
                except ValueError:
                    allints[vname] = False
                    with suppress(ValueError):
                        nval = float(nval)
                if isinstance(nval, int):
                    if nmax.setdefault(vname, float("-inf")) < nval:
                        nmax[vname] = nval
                tmp.append([vname, nval])
            nset.append(tmp)

        while 1:
            with suppress(IndexError):
                if sys.argv[1] == "y":
                    break

            toss = f"Configuration results in {len(nset)} permutations.  Continue? (y/n) > "
            inp = input(toss)
            if not inp:
                continue
            inp = inp[0]
            if inp in ("y", "Y"):
                break
            if inp in ("n", "N"):
                return
            continue

        nlen = len(str(len(nset)))
        for var_index, var_set in enumerate(nset):
            # Create label for output directories
            if flat_dirs:
                _strtag = str(var_index + 1).zfill(nlen)
            else:
                _strtag = Path("")
                for ivar in var_set[1:]:
                    if ivar[0] in allints:
                        fstr = "{0}-{1}"
                    else:
                        fstr = (
                            f"{{0}}-{{1:0{math.ceil(math.log10(nmax[ivar[0]] + 1))}d}}"
                        )
                    _strtag = _strtag / Path(fstr.format(ivar[0], ivar[1]))

            # Create the files and directories from the template
            # Walks the _template_path directory structure
            for root, dirs, files in os.walk(_template_path):
                self.create_output(var_set, root, dirs, files)

            # Wait until there are less than max_threads.
            while _threading.active_count() > max_threads:
                time.sleep(0.1)

            abs_path = Path(_output_path) / _strtag

            os.chdir(abs_path)

            thrd = _threading.Thread(target=self.start_thread_process, args=(program,))
            thrd.start()


# =============================
class Usage(Exception):
    def __init__(self, class_msg):
        self.msg = class_msg


def main(argv=None):
    if argv is None:
        argv = sys.argv

    option_dict = {"debug": 0, "file": ""}
    try:
        opts, _ = getopt.getopt(
            argv[1:], "hvdf:", ["help", "version", "debug", "file="]
        )
    except getopt.error as error_msg:
        raise Usage(error_msg) from error_msg

    for opt in opts:
        if opt[0] in ("-h", "--help"):
            print(f"{modname}: version={__version__}")
            usage()
            sys.exit(0)
        elif opt[0] in ("-v", "--version"):
            print(f"{modname}: version={__version__}")
            sys.exit(0)
        elif opt[0] in ("-d", "--debug"):
            option_dict["debug"] = 1
            sys.argv.remove(opt[0])
        elif opt[0] in ("-f", "--file"):
            option_dict["file"] = opt[1]
            argv.remove(opt[0])
            argv.remove(opt[1])

    # ---make the object and run it---
    main_x = Pyslice()
    main_x.run()


if __name__ == "__main__":
    sys.exit(main())
