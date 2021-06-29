Changes
=======
2013-09-04: v1.7
    * Reworked the documentation
    * Cross compatibility between 2.7 and 3.3 helped out with 'six'.
    * Git didn't do what I want with the moves, but
      * Moved pyslice.py to pyslice/__init__
      * Moved pyslice_lib to pyslice/pyslice_lib
      * Ran 'autopep8' on all files - especially useful on PySPG
    * Added a README.txt that gives some description.
    * Moved to sphinx, restructured text
    * Minor improvements to setup.py to allow 'upload_docs' to work.
    * Finished transition to git.  Deleted CVSROOT and moved everything up
      a directory.
    * Demoed all parts of the functionality in the example.

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
