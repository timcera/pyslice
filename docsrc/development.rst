Architecture
============
The overall process:

+ Parses pyslice.ini file.  'self.read_config()'
+ All quotes within strings in pyslice.ini are removed.  'self.dequote()'
+ All paths are corrected to match the seperator of host machine.  
  'self.path_correction()'
+ Create cartesian of sets for variables specified in pyslice.conf. 
  Now handled by PySPG.
+ Asks user if number of runs is appropriate. If 'n' then bail.
+ Loops on the sets in the cartesian.

  * Loops across all files in template directory.
  
    - Copy any binary files, continue to next file template directory.
      'istext()'
    - For across variable names in pyslice.ini for each line in the file.
  
      + Replace all 
        'keyword' 'Python statement containing variable name' 'keyword' 
        with the evaluation of the Python statement, replacing variable 
        name with correct number from cartesian set.
      + Write out new line to correct output directory and output file.
    - If number of thread is greater than max_processes, wait.
    - Create new thread, use 'os.popen4' to pull output and error from the
      program and put in 'pyslice.log'.


Similar Projects
================
Some templating systems, which I am not going to list here, might be able to be pressed into service, but it was a difficult enough prospect that I wrote Pyslice. The initial push to write Pyslice was my inability to get the Drone software installed an working. Plus Drone was way overkill for what I really needed. 

Here are links to similar projects to Pyslice:

http://pyspg.sourceforge.net/: PySPG: Pyslice uses PySPG as a library to generate values.

http://droneutil.sourceforge.net/, Drone:DroneUtil - part of the Drone system.

http://drone.sourceforge.net/, Drone:Drone - I think a Drone client?

http://droned.sourceforge.net/, Drone:Droned - Drone server.

Changes
=======
2005-08-30: v1.6
Moved to threads rather than 'os.fork/os.exec' which means that pyslice.py should be able to run on Windows, though not tested.  Eliminated a bunch of code required by the 'os.fork/os.exec' that should make pyslice.py easier to maintain.

2005-06-06: v1.5
Uses 'pyslice.ini' instead of 'pyslice.conf'.  This allows the use of .ini editors to easily map to the correct format.

2005-05-30: v1.4
Can pull variable values from statistical distributions in Python's 'random' package. 
Uses os.path.walk to make considerable faster. 
Minor code clean-up 

2004-12-16: v1.3
Now depends on Python 2.x or better. Am now using the PySPG library (http://pyspg.sourceforge.net/) in order to develop the variable sets. Because of PySPG now have the capability of doing geometric and list based parameter generation. 

2001-07-10: v1.1
Removed Python 2.x dependencies. Variables can now use floating point. Works correctly to just create data sets by setting max_processes = 0 in pyslice.conf. Changes to documentation. 

2001-07-10: v1.0
Initial release

Authors
=======
Tim Cera (email: tim @ cerazone dot net)
Initial implementation

Claudio J. Tessone, "http://pyspg.sourceforge.net/", PySPG library

