========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-report-metric/badge/?style=flat
    :target: https://readthedocs.org/projects/python-report-metric
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/iconservo/python-report-metric.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/iconservo/python-report-metric

.. |version| image:: https://img.shields.io/pypi/v/python-report-metric.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/python-report-metric

.. |commits-since| image:: https://img.shields.io/github/commits-since/iconservo/python-report-metric/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/iconservo/python-report-metric/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/python-report-metric.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/python-report-metric

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/python-report-metric.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/python-report-metric

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/python-report-metric.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/python-report-metric


.. end-badges

Unified metric recording

* Free software: MIT license

Installation
============

::

    pip install python-report-metric

Documentation
=============

https://python-report-metric.readthedocs.io/

ENV/CONFIG Variables
====================
Note: In a Django environment, specify these in settings, otherwise use ENV variables.


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
