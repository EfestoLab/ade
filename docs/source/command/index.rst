Command Line usage
##################

.. code-block:: bash

	$ ade

ade command line provides an easy access to the ade module functionalities.
Provides two main modes and a set of optional flags,


..	note::
	In both create and parse actions, the given input data are going to be validated against the regular expressions expressed in the config file.

Modes
=====
Each mode defines a different interaction type with the application.
ade provides 2 main modes, create and parse.

create
------
In order to create a new directory structure you'll need to provide some base data.

.. code-block:: bash

	$ ade create --template @+show+@ --data show=foo sequence=bar shot=zoo --path /tmp

which will print some informations about the process:

.. code-block:: bash

	[INFO][filesystem] - Setting /tmp/foo/vault as 0755
	[INFO][filesystem] - Setting /tmp/foo/temp as 0755
	[INFO][filesystem] - Setting /tmp/foo/editorial as 0755
	[INFO][filesystem] - Setting /tmp/foo/pipeline/config/envs/software.json as 0644
	[..........]
	[INFO][filesystem] - Setting /tmp/foo/python as 0755

.. note::
	Any variable which is not been passed thorugh --data or config file defaults, will be communicated thorugh warning and skipped.

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


--data
-----------------
In order to create a new tree from a template, you need to set some
variable of the templates. Data allowes you to do so.

.. code-block:: bash

	$ ade create --data show=white department=film sequence=AA shot=AA001

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

--config_path
-------------
The path where ade will be looking for the config files.
each config file name will define a ade *mode*.

.. note::
	This variable will ovewrite the $ADE_CONFIG_PATH environment variable

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
