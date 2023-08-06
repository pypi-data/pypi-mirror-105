========
Overview
========

Python wrapper for ThorChain Midgard API

Installation
============

::

    pip install jormungandr

You can also install the in-development version with::

    pip install git+ssh://git@https://gitlab.com/JormThor/Jormungandr/jormthor/Jormungandr.git@master

Documentation
=============


https://Jormungandr.readthedocs.io/


Development
===========

To run all the tests run::

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
