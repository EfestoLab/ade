Examples
========

In order to use ade you'll be in need of using all the prividen classes.


Initialize a config manager
---------------------------
This manager requires only the *config_search_path* to be set, provide access to the configs available.

.. code-block:: python

    import os
    from ade.manager import config as ade_config

    mode = 'default'
    config_path = os.getenv('ADE_CONFIG_PATH')
    config_manager = ade_config.ConfigManager(config_path)
    config_mode = config_manager.get(mode)


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

    template_manager = ade_template.TemplateManager(config_mode)



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

    template_manager = ade_template.TemplateManager(config_mode)
    filesystem_manager = ade_filesystem.FileSystemManager(
        config_mode, template_manager
    )

Create a new paths
------------------
Creating a new path is

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

    data = {'show': 'foo', 'department': 'bar', 'sequence':'AA', 'shot':'00'}
    paths = filesystem_manager.build('@+show+@', data, '/tmp')
    print paths

        > [u'/tmp/mytest_show', u'/tmp/mytest_show/python', u'/tmp/mytest_show/python/2.6.4', u'/tmp/mytest_show/python/2.6.4/modules', u'/tmp/mytest_show/references', u'/tmp/mytest_show/config', u'/tmp/mytest_show/config/envs', u'/tmp/mytest_show/editorial', u'/tmp/mytest_show/temp', u'/tmp/mytest_show/vault']


Parse a new paths
------------------
Creating a new path is

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

    path = '/tmp/mytest_show/guu/AA/AA000/sandbox/hdd/maya/'
    paths = filesystem_manager.parse(path, '@+show+@')

    > [{'department': u'guu', 'show': u'mytest_show', 'shot': u'AA000', 'user': u'hdd', 'sequence': u'AA'}]
