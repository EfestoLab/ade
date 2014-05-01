import os
import json


class ConfigManager(object):
    def __init__(self, config_search_path):

        self.registry = {}

        if not os.path.exists(config_search_path):
            print "{0} doesn't exist".format(config_search_path)
            return

        for root, folders, files in os.walk(config_search_path):
            for _file in files:
                if _file.endswith('json'):
                    config_name = _file.split('.')[0]
                    config_path = os.path.join(root, _file)
                    result = json.load(open(config_path, 'r'))
                    self.registry.setdefault(config_name, result)

c = ConfigManager('../config')
print c.registry
