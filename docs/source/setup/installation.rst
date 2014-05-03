Installation
============

In here you'll learn on how to build install and test the project.

I highly suggest , for the first test installation to use virtualenv, so you can see if all the dependencies are satisfied, before rolling it out in production environments.

.. code-block:: bash

    $ sudo easy_install virtualenv

To build and enable a new env just type:

.. code-block:: bash

    $ cd some/where/
    $ virtualenv ade_test
    $ source ade_test/bin/activate

This should have changed your current shell to something similar to :

.. code-block:: bash

    (ade)$

To exit from the virtual environment type:

.. code-block:: bash

    (ade)$ deactivate

For more informations on how to use `virtualenv <http://www.virtualenv.org/en/latest/>`_ please refer to its documentation.

Download
--------

The main repository of the project lives in bitbucket ad `this <https://bitbucket.org/langeli/filesystemmanager>`_ address:

The code can be downloaded from github with the following command:

.. code-block:: bash

    $ git clone https://langeli@bitbucket.org/langeli/filesystemmanager.git

Build and install
-----------------

In order to build the package you'll need to get into the ade folder and type:

.. note::
    This command will make it also download all the needed packages for having the module working, hence the usage of virtualenv for the first run.

.. code-block:: bash

    $ python setup.py install


Test
----

If you are unsure if the current version is not stable , run the unittests and check for the restult.

.. code-block:: bash

    $ python setup.py test

.. warning::
    If the package is not being installed before running the tests,it will download all the needed packages into the root of the project.

Documentation
-------------

To build the current documentation please run:


.. code-block:: bash

    $ python setup.py build_sphinx

This will produce a build folder into ade/docs which contains the built type (html).

Point your browser to ade/docs/build/html/index.html and you should be able to read this page properly formatted.

.. note::
    If there's any problem on building the docs please ensure that the sphinx module is available.

    If any bug is been found please report it to the `issue tracker <https://bitbucket.org/langeli/filesystemmanager/issues?status=new&status=open>`_.
