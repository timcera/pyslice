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
