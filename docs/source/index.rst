.. Ade documentation master file, created by
   sphinx-quickstart on Sun May 19 00:07:19 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Ade's documentation!
===============================

Ade (ade) is a templated file system tree manager.
Provides the ability to create and parse a tree file structure,
from a set of fragment folders, contained in an arbitrary location. 


Examples
========
Here some simple examples on how use ade:


Create a shot folder into the home directory of the user:
---------------------------------------------------------

.. code-block:: bash

 	$ ade create --data show=white department=dev sequence=AA shot=AA001 --template @+shot+@ --verbose debug --mount_point $HOME


Initialise a new show into a custom path:
-------------------------------------------

.. note::
	mount_point is set to /tmp by default

.. code-block:: bash

 	$ ade create --data show=white --verbose debug --mount_point /jobs --template @+show+@


Create a sandbox folder into the current folder:
------------------------------------------------

.. code-block:: bash

 	$ ade create --mount_point ./ --template @sandbox@  --verbose debug


Parse the given path:
---------------------

.. code-block:: bash

 	$ ade parse --path /tmp/white/job/AF/AF001/sandbox/username/maya/ 
	>> {"department": "job", "show": "white", "shot": "AF001", "user": "username", "sequence": "AF"}


Parse the current path:
---------------------

.. code-block:: bash
	$ cd /tmp/white/job/AF/AF001/sandbox/username/maya/
 	$ ade parse
	>> {"department": "job", "show": "white", "shot": "AF001", "user": "username", "sequence": "AF"}




Contents:

.. toctree::
   :maxdepth: 1

   api/index
   template/index
   command/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
