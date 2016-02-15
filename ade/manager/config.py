import os
import json
from ade.manager.exceptions import ConfigError
from collections import OrderedDict

try:
    import efesto_logger as logging
except:
    import logging


logger = logging.getLogger(__name__)


class ConfigManager(object):
    '''Create and return a ConfigManager instance.

    This object will let you deal with the ade config files:

    :param config_search_path: The path to the config folder.
    :type config_search_path: str

    '''
    def __init__(self, config_search_path):

        self.registry = OrderedDict()
        logger.debug('Using config_search_path: {0}'.format(
            config_search_path
            )
        )

        if not os.path.exists(config_search_path):
            msg = 'config_path {0} does not exist'.format(config_search_path)
            logger.warning(msg)
            raise ConfigError(msg)

        for root, folders, files in os.walk(config_search_path):
            for _file in files:

                if _file.startswith('.'):
                    continue

                if _file.endswith('json'):
                    config_name = _file.split('.')[0]
                    config_path = os.path.join(root, _file)
                    result = json.load(open(config_path, 'r'))
                    self._resolve_envs(result)
                    self.registry.setdefault(config_name, result)

        logger.debug('Config found: {0}'.format(self.registry.keys()))

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

