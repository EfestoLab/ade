Ade
====

 A templated file system manager


Build options
=============

build documentation
-------------
To build the html documentation:

.. code-block:: bash

	python setup.py build_sphinx

Once built use your browser to look into:

.. code-block:: bash

	firefox ./docs/build/html/index.html



Installation
-------------
To install the module, run:

.. code-block::

	python setup.py install

.. note::

    is suggested to install the module in a virtualenv environemnt for testing
    before central installation.


Test
----
To perform the set of unittest for the module.

.. code-block::

	python setup.py test

.. warning::

    The code is not fully tested under windows and it's expecting to break in some cases. If any issue is found please report it to the issue tracker.
