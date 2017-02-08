.. image:: https://travis-ci.org/timcera/pyslice.svg?branch=master
    :target: https://travis-ci.org/timcera/pyslice
    :height: 20

.. image:: https://coveralls.io/repos/timcera/pyslice/badge.png?branch=master
    :target: https://coveralls.io/r/timcera/pyslice?branch=master
    :height: 20

.. image:: https://img.shields.io/pypi/v/pyslice.svg
    :alt: Latest release
    :target: https://pypi.python.org/pypi/pyslice

.. image:: https://img.shields.io/pypi/dm/pyslice.svg
    :alt: PyPI downloads count
    :target: https://pypi.python.org/pypi/pyslice

.. image:: http://img.shields.io/badge/license-BSD-lightgrey.svg
    :alt: pyslice license
    :target: https://pypi.python.org/pypi/pyslice/

Welcome to pyslice - dataset template engine's documentation!
=============================================================
pyslice is a specialized templating system that replaces variables in
a template data set with numbers taken from all combinations of a grouped
series of numbers. It creates a dataset from input template files for each
combination of variables in the series. 

The main function of pyslice is to provide utility functions for parametric
modeling. Parametric modeling is a process of varying many inputs to a model.
A drawback to parametric modeling is that there are usually hundreds to
thousands of data sets to prepare and a corresponding number of model runs.
pyslice will create the model data sets and manage the model runs, or place the
model runs in a queue managed by other software. pyslice is also useful in
establishing the sensitivity of a model to changing parameters. 

Documentation
=============
Reference documentation is at :ref:`pyslice_documentation`.

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

