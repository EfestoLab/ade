Command Line
############

.. code-block:: bash

	$ ade

ade command line provides an easy access to the ade module functionalities.
Provides two main modes and a set of optional flags,

Modes
=====
Each mode defines a different interaction type with the application.
ade provides 2 main modes, parse and create.

parse
-----
In order to parse a tree structure it's matter to run:

.. code-block:: bash

	$ ade parse

and it will parse the current directory against the default tamplate
into the deafault path.

create
------
On another hand creating a tree becomes:

.. code-block:: bash

	$ ade create


Flags
=====

-h
--
Provide a quick help for the available options, and modes.

.. code-block:: bash

	$ ade -h

--mount_point
-------------
Define which is the mount point of the current project.
The mount point is whatever is before /<show>/..../.../

.. code-block:: bash

	$ ade --mount_point /jobs

.. note::
	If not provided, falls back to /tmp.

--template
----------
Specify which template has to be used to build the tree.
The available templates are all the top folder names found in
the defined or default template_folder.

.. code-block:: bash

	$ ade --template @+show+@

.. note::
	If not provided, falls back to the default and included
	template definition set.


--data
-----------------
In order to create a new tree from a template, you need to set some
variable of the templates. Data allowes you to do so.

.. code-block:: bash

	$ ade create --data show=white department=film sequence=AA shot=AA001

.. note::
	If not provided , a set of environment variables are used as lookup.

	* show = $SHOW
	* department = $DEPARTMENT
	* sequence = $SEQUENCE
	* shot = $SHOT
	* user = $USER


--template_folder
-----------------
The template folder is where the various template fragments are collected.

.. code-block:: bash

	$ ade --template_folder /somewhere/on/disk

--verbose
---------
Set the verbosity level for the application, to get sensible detail enable
the debug mode.

Available levels:

* info
* debug
* warning
* error

.. code-block:: bash

	$ ade create --verbose debug

--path
------

The target path for the parse or create.

.. code-block:: bash

	$ ade parse --path /tmp/white/AF/AF001/maya/scenes

