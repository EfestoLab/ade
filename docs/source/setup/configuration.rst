Configuration
=============

In order to run properly, ade requires some setting and configuration files to be put in place.

Environment variables
---------------------

An environment variable to the config folder is required in order to discover the available configuration files.

.. code-block:: bash

    export ADE_CONFIG_PATH=/path/to/../resources/config

To see if the environment is correctly set type:

.. code-block:: bash

    echo $ADE_CONFIG_PATH


Config File
-----------
The content of this fill will drive the overall behaviour of ade.

.. literalinclude:: default.json
   :language: json


project_mount_point
...................
This will validate the path you are working in is supposed to be a templated path, and where it starts from.


template_search_path
....................
In this path, ade will search for the templates to be used.
in this example, the path will set against the $ADE_CONFIG_PATH variable.

.. note::
    It is fairly common that the template folder will live next to the config folder. The value "$ADE_CONFIG_PATH/../templates , will set it as such.


defaults
........
Some of the needed data to build a structure can be provided through this set of environment variables replacements.

each remplacement will be defined as :

.. code-block:: json

    {
    "<name>": "<$ENVIRONMENT>"
    }

eg:

.. code-block:: json

    {
    "user" : "$USER"
    }


regexp_mapping
..............
In here you'll be able to define how each variable fragment (+<something>+) ,
will be validated against on creation and parse, if not providen , it won't be matched.


.. code-block:: json

    {
    "<name>": "<regular_expression>"
    }

eg:


.. code-block:: json

    {
    "sequence": "(?P<sequence>[a-zA-Z0-9_]+)"
    }

In this case, during the creation and the parse, the fragment @+sequence+@ will be validated against this regular expression value.
