Example
=======

In this page we are going to create a full Ade structure for some fictional entities from scratch. This is a recap of what we will be needing of:

1. A config file
    * A mount point. This is where Ade will be constrained to create the folder structure.
    * Regex to extract information
2. An Ade template. The one used in this example can be downloaded :download:`here <../example/ade_template.zip>`.
3. Some data to fill the dynamic folder names.


First, we are going to define our fake data:

.. code-block:: bash

    Show: Foo
        Sequence: Bar
            Shot: 001
            Shot: 002
        Sequence: Baz
            Shot: 001
            Shot: 002
        Asset: Spam
        Asset: Eggs


Let's start creating the base Ade configuration structure:

.. code-block:: bash
    
    $ cd ~/Desktop
    $ mkdir ade_config
    $ touch ade_config/default.json
    $ mkdir ade_config/ade_template


Now, we are going to create the template. The template works with basic syntax for the folder names dynamic generation and a really simple inheritance system. We will start from top to bottom, hence, the Show will be the first to be created:

.. code-block:: bash
    
    $ cd ade_config/ade_template
    $ mkdir @+show+@

Now, let's create the sequences and shots:

.. code-block:: bash

    $ mkdir @+sequence+@
    $ mkdir @+shot+@
    $ mkdir @+show+@/@+sequence+@
    $ mkdir @+sequence+@/@+shot+@

.. note::
    
    We create twice the folders because every dynamic folders needs to be defined in an index, in this case the root template path.

And now the assets:

.. code-block:: bash

    $ mkdir @Assets@
    $ mkdir @+asset+@
    $ mkdir @Assets@/@+asset+@
    $ mkdir @+show+@/@Assets@


.. note::

    ``@*@`` defines a folder with dynamic content but static name, whereas ``@+*+@`` defines a folder with both content and name dynamic.


To do a quick recap, what we have done in plain english is the following:

* Define a ``show``, ``sequence``, ``shot`` and ``asset`` variables
* Set the content of ``show`` to ``Assets`` and ``sequence``, the content of ``sequence`` to ``shot`` and the content of ``Assets`` to ``asset``.

Now, we'll set up a mount point:

.. code-block:: bash

    $ cd ~/Desktop
    $ mkdir my_projects


Finally we'll be filling up the configuration file. These are the bare minimum requirements we need:

1. ``project_mount_point``: A project mount point where to create the folders.
2. ``template_search_path``: Where are we going to read the template from.
3. ``regexp_mapping``: How to extract the information from the variables.

Our configuration file should look like this:

.. code-block:: json

    {
        "project_mount_point": "$HOME/Desktop/my_projects",
        "template_search_path": "$HOME/Desktop/ade_config/ade_template",
        "regexp_mapping" : {
                "show": "(?P<show>[a-zA-Z0-9_]+)",
                "sequence": "(?P<sequence>[a-zA-Z0-9_]+)",
                "shot": "(?P<shot>[a-zA-Z0-9_]+)",
                "asset": "(?P<shot>[a-zA-Z0-9_]+)"
            },
        "defaults": {}
    }


Now for the last final bit:

.. code-block:: bash

    $ export ADE_CONFIG_PATH=$HOME/Desktop/ade_config

For speed's sake, we'll be using ade from Python in this last bit.

.. note::
    
    All Ade Python documentation can be found at :doc:`../reference/examples`


.. code-block:: python

    import os
    from ade.manager import config as ade_config
    from ade.manager import template as ade_template
    from ade.manager import filesystem as ade_filesystem

    mode = 'default'
    config_path = os.getenv('ADE_CONFIG_PATH')

    config_manager = ade_config.ConfigManager(config_path)
    config_mode = config_manager.get(mode)

    template_manager = ade_template.TemplateManager(config_mode)
    filesystem_manager = ade_filesystem.FileSystemManager(
        config_mode, template_manager
    )

    data = []

    data.append({'show': 'Foo', 'sequence': 'Bar', 'shot': '001'})
    data.append({'show': 'Foo', 'sequence': 'Bar', 'shot': '002'})
    data.append({'show': 'Foo', 'sequence': 'Baz', 'shot': '001'})
    data.append({'show': 'Foo', 'sequence': 'Baz', 'shot': '002'})
    data.append({'show': 'Foo', 'asset': 'Spam'})
    data.append({'show': 'Foo', 'asset': 'Eggs'})

    for datum in data:
        filesystem_manager.build(
            '@+show+@',
            datum,
            config_mode['project_mount_point']
        )

Now our folder structure is constructed.
