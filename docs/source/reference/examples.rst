Examples
========

In order to use ade you'll be in need of using all the prividen classes.


Initialize a config manager
---------------------------
This manager requires only the *config_search_path* to be set, provide access to the configs available.

.. code-block:: python

    import os
    from ade.manager import config as ade_config

    config_path = os.getenv('ADE_CONFIG_PATH')
    ade_config.ConfigManager(config_path)


Initialize a template manager
-----------------------------
This template requires a config mode to be initialized.
Summing this to the previous step you'll end up having:

.. code-block:: python

    import os
    from ade.manager import config as ade_config
    from ade.manager import template as ade_template

    mode = 'default'
    config_path = os.getenv('ADE_CONFIG_PATH')

    config_manager = ade_config.ConfigManager(config_path)
    config_mode = config_manager.get(mode)

    template_manager = ade_template.TemplateManager(config_manager)



Initialize a filesystem manager
-------------------------------
The final step is now to create the last manager, which will let you create and parse the paths you need.

.. code-block:: python

    import os
    from ade.manager import config as ade_config
    from ade.manager import template as ade_template
    from ade.manager import filesystem as ade_filesystem

    mode = 'default'
    config_path = os.getenv('ADE_CONFIG_PATH')

    config_manager = ade_config.ConfigManager(config_path)
    config_mode = config_manager.get(mode)

    template_manager = ade_template.TemplateManager(config_manager)
    filesystem_manager = ade_filesystem.FileSystemManager(
        config_manager, template_manager
    )

Create a new paths
------------------


.. code-block:: python

    import os
    from ade.manager import config as ade_config
    from ade.manager import template as ade_template
    from ade.manager import filesystem as ade_filesystem

    mode = 'default'
    config_path = os.getenv('ADE_CONFIG_PATH')

    config_manager = ade_config.ConfigManager(config_path)
    config_mode = config_manager.get(mode)

    template_manager = ade_template.TemplateManager(config_manager)
    filesystem_manager = ade_filesystem.FileSystemManager(
        config_manager, template_manager
    )

    data = {'show': 'foo', 'discipline': 'bar', 'sequence':'AA', 'shot':'00'}
    filesystem_manager.build('@+show+@', data, '/tmp')

