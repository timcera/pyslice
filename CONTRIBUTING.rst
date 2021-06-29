============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Development is managed on bitbucket at
   https://bitbucket.org/timcera/pyslice/overview.

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


Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://bitbucket.org/timcera/pyslice

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the bitbucket issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the bitbucket issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

pyslice could always use more documentation, whether as part of the
official pyslice docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://bitbucket.org/timcera/pyslice

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `pyslice` for local development.

1. Fork the `pyslice` repo on bitbucket.
2. Clone your fork locally::

    $ git clone git@bitbucket.org:your_bitbucket_login/pyslice.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv pyslice
    $ cd pyslice/
    $ python setup.py develop

4. For testing you also need to install tox, coverage, and flake8::

    $ pip install tox
    $ pip install coverage
    $ pip install flake8

5. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

6. When you're done making changes, check that your changes pass flake8 and the
tests, including testing other Python versions with tox::

    $ tox

Bring the htmlcov/index.html file up into a browser to make sure that the code has appropriate test coverage.

7. Commit your changes and push your branch to bitbucket::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

8. Submit a pull request through the bitbucket website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.7, and 3.3.
