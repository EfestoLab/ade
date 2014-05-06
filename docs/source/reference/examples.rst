Examples
========

In order to use ade you'll be in need of using all the prividen classes.


Initialise a config manager
---------------------------
This manager requires only the *config_search_path* to be set, provide access to the configs available.

.. code-block:: python

    import os
    from ade.manager import config as ade_config

    config_path = os.getenv('ADE_CONFIG_PATH')
    ade_config.ConfigManager(config_path)


Initialise a template manager
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

    emplate_manager = ade_template.TemplateManager(config_manager)


