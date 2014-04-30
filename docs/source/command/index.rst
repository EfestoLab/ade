Command Line
############

.. code-block:: bash

	$ ade

ade command line provides an easy access to the ade module functionalities.
Provides two main modes and a set of optional flags,

Modes
=====
Each mode defines a different interaction type with the application.
ade provides 2 main modes, create and parse.

create
------
In order to create a new directory structure you'll need to provide some base data.

.. code-block:: bash

	$ ade create --template @+show+@ --data show=foo sequence=bar shot=zoo --path /tmp --mount_point=/tmp

which will print some informations about the process:

.. code-block:: bash

	[WARNING][filesystem] - 'python_version' not found for {show}/python/{python_version}
	[WARNING][filesystem] - 'python_version' not found for {show}/python/{python_version}/modules
	[INFO][filesystem] - Setting /tmp/foo/vault as 0755
	[INFO][filesystem] - Setting /tmp/foo/temp as 0755
	[INFO][filesystem] - Setting /tmp/foo/editorial as 0755
	[INFO][filesystem] - Setting /tmp/foo/pipeline/config/envs/software.json as 0644
	[..........]
	[INFO][filesystem] - Setting /tmp/foo/python as 0755

.. note::
	In this case the warning are related to a missing variable (--data python_version=2.6.4) required to build the default template @+show+@

parse
-----
.. note::
	This function will return a json encoded string ready to be passed to any other interpreter which is able to accept it.

Same for parsing them back :

.. code-block:: bash

	$ ade parse --path /tmp/foo/pipeline/rnd/config/envs --template @+show+@
	{"department": "pipeline", "show": "foo", "sequence": "rnd"}


Being the default path set to ./ , and @+show+@ the default schema, you'll be able to simply do from within any of the project folder:

.. code-block:: bash

	$ cd /tmp/foo/pipeline/rnd/config/envs
	$ ade parse
	{"department": "pipeline", "show": "foo", "sequence": "rnd"}

Flags
=====

-h
--
Provide a quick help for the available options, and modes.

.. code-block:: bash

	$ ade -h

--path
------

The target path for the parse or create.

.. code-block:: bash

	$ ade parse --path /tmp/white/AF/AF001/maya/scenes


--mount_point
-------------

The root path of the project, usually the mount point.

.. note::

	This is set to the default value of /tmp

.. code-block:: bash

	$ ade parse --path /tmp/white/AF/AF001/maya/scenes

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
