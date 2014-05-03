Configuration
=============

In order to run properly, ade requires some setting and configuration files to be put in place.

An environment variable to the config folder is required in order to discover the available configuration files.

Environment variables
---------------------

.. code-block:: bash

    export ADE_CONFIG_PATH=/path/to/../resources/config


Config File
-----------
Each configuration file, will have to respect this structure:

.. literalinclude:: default.json
   :language: json


Here some fields details:

project_mount_point
...................


template_search_path
....................


defaults
........


regexp_mapping
..............
