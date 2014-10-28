===============
pytest-smartcov
===============

Smart coverage measurement and reporting for py.test test suites.

Test suites are usually structured parallel to (or integrated with) the
structure of the code they test. If you ask py.test to run a certain subset of
your tests, you shouldn't have to also tell coverage which subset of your code
it should measure coverage on for that run. With ``pytest-smartcov``, you don't
have to.


Prerequisites
=============

``pytest-smartcov`` requires Python 2.7 or higher and `coverage`_ 3.6 or higher.

.. _coverage: http://nedbatchelder.com/code/coverage/


Usage
=====

If ``pytest-smartcov`` is installed and you provide a ``smartcov_paths_hook``
setting in your ``pytest.ini``, coverage will automatically be measured on all
your test runs, unless you provide the ``--no-cov`` flag.


Configuration
-------------

To use ``pytest-smartcov``, provide a ``smartcov_paths_hook`` ini-config
setting which is the Python dotted import path to a function. This function
should accept as its single parameter the list of test paths specified on a
``py.test`` command line, and should return the list of paths on which code
coverage will be measured.


Reporting
---------

If 100% of the measured code was covered, ``pytest-smartcov`` will output a
single line at the end of test run notifying you that you have 100% coverage.

If you have less than 100% coverage on the measured code, ``pytest-smartcov``
will output a terminal report including only those files which had less than
100% coverage.

If there was less than 100% overall coverage, ``pytest-smartcov`` will also
output an HTML report (to the ``htmlcov/`` directory by default, though this
can be configured normally in ``.coveragerc``).
