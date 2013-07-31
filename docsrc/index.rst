.. Pyslice - dataset template engine documentation master file, created by
   sphinx-quickstart on Tue Mar  8 19:27:37 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pyslice - dataset template engine's documentation!
=============================================================

Pyslice is a specialized templating system that replaces variables in a template data set with numbers taken from all combinations of a grouped series of numbers. It creates a dataset from input template files for each combination of variables in the series. 

The main function of Pyslice is to provide utility functions for parametric modeling. Parametric modeling is a process of varying many inputs to a model. A drawback to parametric modeling is that there are usually hundreds to thousands of data sets to prepare and a corresponding number of model runs. Pyslice will create the model data sets and manage the model runs, or place the model runs in a queue managed by other software. Pyslice is also useful in establishing the sensitivity of a model to changing parameters. 

Contents:

.. toctree::
   :maxdepth: 2

   install
   manual
   development


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

