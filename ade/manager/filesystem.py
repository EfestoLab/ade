'''
FileSystemManager manager

Construct and parse results of the teplate manager

'''
import os
import re
import logging
from pprint import pformat
from ade.exception import ConfigError


class FileSystemManager(object):
    ''' Return an instance of FileSystemManager.

    :param config: the config for the project.
    :type config: dict
    :param template_manager: An instance of the templateManager.
    :type template_manager: TemplateManager

    '''

    def __init__(self, config, template_manager):
        self.log = logging.getLogger('ade')

        self.template_manager = template_manager

        self.mount_point = config['project_mount_point']

        self.default_field_values = config['defaults']
        self.regexp_mapping = config['regexp_mapping']

    def build(self, name, data, path):
        ''' Build the given schema name, and replace data,
        level defines the depth of the built paths.

        :param name: The template *name* to build.
        :type name: str
        :param data: A set of data to create the template with.
        :type name: dict
        :param path: the path where the structure has to be created.
        :type name: str
        '''
        current_path = path or self.mount_point
        current_path = os.path.realpath(current_path)

        self.log.debug('Building template : {0} in : {1}'.format(
            name, current_path)
        )

        if not self.mount_point in current_path:
            self.log.error(
                ('Structure can not be created'
                 ' outside of mount_point {0}').format(self.mount_point)
            )
            return

        if not os.path.exists(current_path):
            self.log.error('Path {0} does not exist.'.format(self.mount_point))
            return

        built = self.template_manager.resolve_template(name)
        results = self.template_manager.resolve(built)
        path_results = self._to_path(results, data)
        for result in path_results:
            path = os.path.join(current_path, result['path'])
            try:
                if result['folder']:
                    #: Create the folder
                    self.log.debug('creating folder: {0}'.format(path))
                    os.makedirs(path)
                else:
                    self.log.debug('creating file: {0}'.format(path))
                    file_content = result['content']
                    with open(path, 'w') as file_data:
                        file_data.write(file_content)

            except (IOError, OSError) as error:
                self.log.debug('{0}'.format(error))
                pass

        #: Set permissions, using the reversed results
        for result in reversed(path_results):
            path = os.path.join(current_path, result['path'])
            permission = result['permission']
            permission = int(permission, 8)
            self.log.info('Setting {1} as {0}'.format(
                oct(permission), os.path.realpath(path)
            ))
            try:
                os.chmod(path, permission)
            except OSError, error:
                self.log.debug(error)

    def parse(self, path, name):
        ''' Parse the provided path against
        the given schema name.

        :param path: The *path* to be parsed.
        :type path: str
        :param name: The teplate name to parse against.
        :type name: str

        '''
        if not path.startswith(self.mount_point):
            self.log.exception(
                ('The path %s does not seems contained'
                 ' in the given mount_point %s') % (
                    path, self.mount_point
                )
            )
            return

        path = path.split(self.mount_point)[-1]
        if path.startswith(os.sep):
            path = path[1:]

        self.log.debug('Parsing {0} against {1}'.format(name, path))
        matched_results = []
        built = self.template_manager.resolve_template(name)
        results = self.template_manager.resolve(built)
        parsers = self._to_parser(results)
        for parser in parsers:
            check = re.compile(parser)
            match = check.match(path)
            if not match:
                continue

            self.log.debug('Match found for {0} with {1}'.format(
                path, parser
            ))
            result = match.groupdict()
            if result and result not in matched_results:
                matched_results.append(result)
            break

        matched_results.sort()
        matched_results.reverse()
        return matched_results

    def _to_parser(self, paths):
        ''' Recursively build a parser from the
        given set of schema paths

        '''
        result_paths = []
        for path in paths:
            result_path = []
            path = path['path']
            for entry in path:
                if '+' in entry:
                    entry = entry.split('+')[1]
                    parser = self.regexp_mapping.get(
                        entry
                    )
                    try:
                        entry = parser.format(entry)
                    except AttributeError:
                        raise ConfigError(
                            'Regular expression not found for: {0}'.format(
                                entry
                            )
                        )
                result_path.append(entry)

            # Enforce checking with ^$
            result_path = '^{0}$'.format((os.sep).join(result_path))
            result_paths.append(result_path)

        result_paths.sort(key=len)
        return result_paths

    def _validate_data(self, data):
        # validate build folder against regexps
        for name, value in data.items():
            if name in self.regexp_mapping:
                regexp = re.compile(self.regexp_mapping[name])
                match = regexp.match(value)
                if not match:
                    self.log.warning(
                        'Value {1} for data {0} does not match {2}'.format(
                            name, value, self.regexp_mapping[name]
                        )
                    )
                    data.pop(name)

    def _set_default_values(self, data):
        for name, value in self.default_field_values.items():
            if name in data:
                data[name] = os.getenv(self.default_field_values[name])

    def _to_path(self, paths, data):
        ''' Recursively build a list of paths from the given
        set of schema paths.

        '''
        data = data or {}
        self._set_default_values(data)
        self._validate_data(data)
        result_paths = []
        for entry in paths:
            result_path = []
            for item in entry['path']:
                if '+' in item:
                    item = item.split('+')[1]
                    item = '{%s}' % item
                result_path.append(item)

            if result_path not in result_paths:
                final_path = (os.sep).join(result_path)
                try:
                    final_path = final_path.format(**data)

                except Exception, error:
                    self.log.warning('{1} not found for {0}'.format(
                        final_path,
                        error
                        )
                    )
                    continue
                entry['path'] = final_path
                result_paths.append(entry)

        return result_paths
