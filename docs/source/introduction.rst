Introduction to Ade
===================

How does it work?
-----------------

Ade is meant for replicating a folder structure which has variable names on each folder level. It is based on a template (specified in a configuration file) made with folders. Given the folder structure:

.. code-block:: bash
    
    $ tree .
    .
    |-- @+asset+@
    |   `-- foo
    `-- @+show+@
        `-- @+asset+@


The template manager will be able to generate:

.. code-block:: bash
    
    @+show+@
    @+show+@/@+asset+@
    @+show+@/@+asset+@/foo

Once we have all this paths generated, when given some data to a :class:`FileSystemManager`, all this virtual folders will be populated with that data and formatted accordingly.

For example, given this data:

.. code-block:: json

    {
        "show": "spam",
        "asset": "eggs"
    }

Ade will generate:

.. code-block:: bash
    
    spam
    spam/eggs
    spam/eggs/foo

Ade requires three main components, in which all the logic is contained:

1. :class:`ade.manager.config.ConfigManager`: This will scan the paths specified in the ``ADE_CONFIG_PATH`` environment variable and it will register all configuration files (``*.json``) found there. This class will contain the configuration for the Ade session.
2. :class:`ade.manager.template.TemplateManager`: This class, with a :class:`ade.manager.config.ConfigManager` instance, will generate a virtual unformatted list of directories to be created.
3. :class:`ade.manager.filesystem.FileSystemManager`: This class will format the folders and create them in the specified mount point.
