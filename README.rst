.. image:: https://travis-ci.org/timcera/pyslice.svg?branch=master
    :target: https://travis-ci.org/timcera/pyslice
    :height: 20

.. image:: https://coveralls.io/repos/timcera/pyslice/badge.png?branch=master
    :target: https://coveralls.io/r/timcera/pyslice?branch=master
    :height: 20

.. image:: https://pypip.in/v/pyslice/badge.png?style=flat
    :alt: Latest release
    :target: https://pypi.python.org/pypi/pyslice

.. image:: https://pypip.in/d/pyslice/badge.png?style=flat
    :alt: PyPI downloads count
    :target: https://pypi.python.org/pypi/pyslice

.. image:: https://pypip.in/license/pyslice/badge.png?style=flat
    :alt: pyslice license
    :target: https://pypi.python.org/pypi/pyslice/

Welcome to Pyslice - dataset template engine's documentation!
=============================================================
Pyslice is a specialized templating system that replaces variables in a template data set with numbers taken from all combinations of a grouped series of numbers. It creates a dataset from input template files for each combination of variables in the series. 

The main function of Pyslice is to provide utility functions for parametric modeling. Parametric modeling is a process of varying many inputs to a model. A drawback to parametric modeling is that there are usually hundreds to thousands of data sets to prepare and a corresponding number of model runs. Pyslice will create the model data sets and manage the model runs, or place the model runs in a queue managed by other software. Pyslice is also useful in establishing the sensitivity of a model to changing parameters. 

Documentation
=============
Reference documentation is at http://pythonhosted.org/pyslice/

Installation
============

At the command line::

    $ pip install pyslice
    # OR
    $ easy_install pyslice
 
Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv pyslice
    $ pip install pyslice

Development
===========
Development is managed on bitbucket at
https://bitbucket.org/timcera/pyslice/overview.

