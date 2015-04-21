import os
import json
import logging
from pprint import pformat
from ade.manager.exceptions import ConfigError
from ade.helper import setup_custom_logger


class ConfigManager(object):
    '''Create and return a ConfigManager instance.

    This object will let you deal with the ade config files:

    :param config_search_path: The path to the config folder.
    :type config_search_path: str

    '''
    def __init__(self, config_search_path):
        self.log = setup_custom_logger('ade')

        self.registry = {}
        self.log.debug('Using config_search_path: {0}'.format(
            config_search_path
            )
        )

        if not os.path.exists(config_search_path):
            raise ConfigError(
                'config_path {0} does not exist'.format(config_search_path)
            )

        for root, folders, files in os.walk(config_search_path):
            for _file in files:
                if _file.endswith('json'):
                    config_name = _file.split('.')[0]
                    config_path = os.path.join(root, _file)
                    result = json.load(open(config_path, 'r'))
                    self._resolve_envs(result)
                    self.registry.setdefault(config_name, result)

        self.log.debug('Config found: {0}'.format(self.registry.keys()))

    def _resolve_envs(self, config):
        for k, v in config.items():
            if isinstance(v, dict):
                self._resolve_envs(v)

            if isinstance(v, basestring):
                path = os.path.expandvars(v)
                if os.path.exists(path):
                    path = os.path.realpath(path)

                config[k] = path

    @property
    def modes(self):
        ''' The available modes of available.
        '''
        return self.registry.keys()

    def get(self, profile):
        if profile not in self.registry:
            raise ConfigError('config profile {0} not found'.format(profile))

        return self.registry[profile]

