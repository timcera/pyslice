.. include:: ../BADGES.rst
.. Manual

===========
User Manual
===========

Overview
========

Pyslice creates input data sets from a template, replacing variables in the
template files with a set of values.  It then runs the desired model against
each created data set, keeping simultaneous model runs below a specified
threshold or submitting jobs to a seperate queueing software.  It is an ideal
program when hundreds of runs are required.  Example uses would be for
calibration or sensitivity analysis.  The input data set creation feature can
easily be setup to create thousands of data sets.

See the example directory under the pyslice install directory for an example
pyslice.ini, template_path (equal to 'input_template), and output_path (equal
to 'output') directories.  To run the example, type 'python ../pyslice.py' (or
'./go' which does the same thing) from within the 'example' directory.

::

    cd pyslice
    cd example             # so that pyslice.py can find the pyslice.ini
    python ../pyslice.py   # or './go'

After answering the questions, directories will begin to appear in the
'example/output' directory based on template files in the
'example/input_template' directory and the configuration in 'pyslice.ini'.

Configuration File: pyslice.ini
===============================
Pyslice requires a configuration file named 'pyslice.ini'.  Sections
are identified with square brackets.  Parameters are set within each
section with the format 'parameter=value'.  This is a standard '.ini' file described in the ConfigParser Documentation <"http://www.python.org/doc/current/lib/module-ConfigParser.html">.

The 'pyslice.ini' file requires the sections, 'paths', 'flags', and 'program'.
There must be at least one variable section.  The variable section(s) can be
named with any valid Python name (start with letter or underscore and can
contain numbers, letters and underscores).

The following example pyslice.ini will take all files in the
template_path directory, replacing the variables 'flow', 'function',
'pressure', and 'salinity' within each file.  Note that the set does
not included the stop value.

::

    [paths]
    # 'template_path' can contain any number of files.  Pyslice even
    #                 correctly handles binary files (just copies them)
    #                 and permissions.
    # 'output_path' is the directory where the output datasets, in their
    #               own sub-directories will be created.
    template_path=/path/to/directory/holding/the/template/datasets
    output_path=/path/to/where/output/directories/will/be/made

    # [flags] identify global options
    # 'keyword' can be changed if '$$' means something in your datasets
    #           'keyword' is used to bracket the Python code to have
    #           pyslice.py evaluate.
    # 'max_threads'   should be set to 1 if you just want all the jobs
    #                 to be run.  This is useful if you have seperate
    #                 queueing software.  Otherwise set to the number
    #                 of simultaneous model runs you can allow on your
    #                 machine.
    # 'flat_dirs' gives the option of whether or not to have numbered
    #             output directories or a directory tree using the variable
    #             values.
    [flags]
    keyword="$$"
    max_threads=8
    flat_dirs="N"

    # [program] is the command you want run in each of the output
    #           directories.
    [program]
    program="model -f "

    # [flow] is set to 90, 92, 94, 96, 98
    # 'arithmetic' is (increment + previous_value)
    [flow]
    type=arithmetic
    start=90
    stop=100
    increment=2

    # [function] is set to 5, 10, 20, 40
    # 'geometric' is (increment * previous_value)
    [function]
    type=geometric
    start=5
    stop=41
    increment=2

    # [pressure] is set to 1, 20, 24, 5, 8
    # 'list' takes the values in turn
    # 'value_type' can be int, float, or str
    # 'value####' must be the type in 'value_type'
    [pressure]
    type=list
    value_type=int
    values_list=[1,20,24,5,8]

    # [rstage] is set to 'samples' values taken from distribution
    # 'distribution' is the statistical distribution from the random
    # module
    #     uniform(a, b) - Get a random number in the range [a, b).
    #     randint(a, b) - Return random integer in range [a, b],
    #         including both end points.
    #     betavariate(alpha, beta) - Beta distribution.  Conditions
    #         on the parameters are alpha > -1 and beta} > -1.
    #         Returned values range between 0 and 1.
    #     choice(seq) -  Choose a random element from a non-empty
    #         sequence.
    #     expovariate(lambd) - Exponential distribution.  lambd is
    #         1.0 divided by the desired mean.  (The parameter would
    #         be called "lambda", but that is a reserved word in
    #         Python.)  Returned values range from 0 to positive
    #         infinity.
    #     gammavariate(alpha, beta) - Gamma distribution.  Not the
    #         gamma function!  Conditions on the parameters are
    #         alpha > 0 and beta > 0.
    #     gauss(mu, sigma) - Gaussian distribution.  mu is the mean,
    #         and sigma is the standard deviation.  This is slightly
    #         faster than the normalvariate() function.
    #     lognormvariate(mu, sigma) - Log normal distribution.  If
    #         you take the natural logarithm of this distribution,
    #         you'll get a normal distribution with mean mu and
    #         standard deviation sigma.  mu can have any value, and
    #         sigma must be greater than zero.
    #     normalvariate(mu, sigma) - Normal distribution.  mu is the
    #         mean, and sigma is the standard deviation.
    #     paretovariate(alpha) - Pareto distribution.  alpha is the
    #         shape parameter.
    #     random(...) random() -> x in the interval [0, 1).
    #     vonmisesvariate(mu, kappa) - Circular data distribution.
    #         mu is the mean angle, expressed in radians between 0
    #         and 2*pi, and kappa is the concentration parameter,
    #         which must be greater than or equal to zero.  If kappa
    #         is equal to zero, this distribution reduces to a
    #         uniform random angle over the range 0 to 2*pi.
    #     weibullvariate(alpha, beta) - Weibull distribution.  alpha
    #         is the scale parameter and beta is the shape parameter.
    # 'samples' is the number of samples taken from the distribution
    [rstage]
    type=montecarlo
    distribution=uniform(50, 1000000)
    samples=100

Template Directory
==================
All files in the 'template_path' directory will be processed by
replacing each instance of

 <keyword> <Python statement that can use variables in pyslice.ini> <keyword>

in EVERY text file.  Binary files are copied, without processing, to the target directory.

The keyword string (default is '$$') and variable names are specified in pyslice.ini.

An example template file::

     T1 Simulation of salinity in the No Name River
     T2 with flow = $$flow$$
     # Any valid Python statement can be used
     F1 $$'%10.3f' % flow$$
     F2 46.58 $$'%10.3f' % (flow * 100)$$
     F3 $$flow$$ 35.679 $$'%d' % flow$$

with the example 'pyslice.ini' file above, would result in the
following file in the output_path/00000 directory if the flat_dirs
option is set, otherwise an entire directory tree is created that
incorporates the variable names and the values::

     T1 Simulation of salinity in the No Name River
     T2 with flow = 90
     # Any valid Python statement can be used
     F1     90.000
     F2 46.58   9000.000
     F3 90 35.679 90

and the next directory in output_path::

     T1 Simulation of salinity in the No Name River
     T2 with flow = 92
     # Any valid Python statement can be used
     F1     92.000
     F2 46.58   9200.000
     F3 92 35.679 92

...etc.

Table of example code in template files, 'flow' varies from 1 to 3 by 1 and 'water_level' varies from 9 to 12 by 1.

+---------------------------+---------+-----------+------------------+
|Example Template Code      |Output   |Flow Result|Water Level Result|
|                           |Directory|Flow Result|Water Level Result|
+===========================+=========+===========+==================+
| | $$'%10.4f' % flow$$     |00000    |1.0000     |9                 |
| | $$water_level$$         +---------+-----------+------------------+
|                           |00001    |1.0000     |10                |
|                           +---------+-----------+------------------+
|                           |00002    |1.0000     |11                |
|                           +---------+-----------+------------------+
|                           |00003    |2.0000     |9                 |
|                           +---------+-----------+------------------+
|                           |00004    |2.0000     |10                |
|                           +---------+-----------+------------------+
|                           |00005    |2.0000     |11                |
+---------------------------+---------+-----------+------------------+
| | $$'%10.4f' % (flow*.1)$$|00000    |0.1000     |1.8               |
| | $$(water_level*0.2)$$   +---------+-----------+------------------+
|                           |00001    |0.1000     |2.0               |
|                           +---------+-----------+------------------+
|                           |00002    |0.1000     |2.2               |
|                           +---------+-----------+------------------+
|                           |00003    |0.2000     |1.8               |
|                           +---------+-----------+------------------+
|                           |00004    |0.2000     |2.0               |
|                           +---------+-----------+------------------+
|                           |00005    |0.2000     |2.2               |
+---------------------------+---------+-----------+------------------+

Tips and Tricks
===============
If you want a model data set with a constant value, just manipulate
the start and end values.
If you want several repetitions of the entire parameterization create
a false variable that isn't used in any of the templates.  This would
be useful if the model imposes some random behavoir that you want to
study.
Another solution to obtain multiple repetitions is rerun pyslice with
different output directories.

Mini Python Reference: Old Style String Formatting
==================================================

Python controls the format of a number through the following syntax:

'format_string' % number

If you want to make a calculation you must enclose the calculation in
'()'.

Python number formatting is illustrated in the following table:

+----------+---------+----------------+-----------------+-----------+
| Format   | Format  | Definition     | Example         | Result    |
|          | String  |                |                 |           |
+==========+=========+================+=================+===========+
| Floating | '%m.nf' | m=total width  | '%10.3f' % 12.2 | 12.200    |
| point    | '%m.nf' | m=total width  | '%10.3f' % 12.2 | 12.200    |
|          |         | n=places after |                 |           |
|          |         | decimal        |                 |           |
+----------+---------+----------------+-----------------+-----------+
| Integer  | '%md'   | m=total width  | '%10d' % 12.2   |        12 |
+----------+---------+----------------+-----------------+-----------+

For additional detail refer to Python String Formatting Operations <"http://docs.python.org/lib/typesseq-strings.html#l2h-211">.

Users Manual Disclaimer
-----------------------
I have manual writers block.  Frankly if anyone can figure out how to
operate pyslice from this manual, they are smarter than I am.  :-)  I
really want suggestions about how to make this clearer.  Send me a
note!
