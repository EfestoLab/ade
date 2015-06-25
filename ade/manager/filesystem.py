'''
FileSystemManager manager

Construct and parse results of the teplate manager

'''
import os
import re
from pprint import pformat
from ade.manager.exceptions import ConfigError
from collections import OrderedDict

try:
    import efesto_logger as logging
except:
    import logging


log = logging.getLogger(__name__)


class FileSystemManager(object):
    ''' Return an instance of FileSystemManager.

    :param config: the config for the project.
    :type config: dict
    :param template_manager: An instance of the templateManager.
    :type template_manager: TemplateManager

    '''

    def __init__(self, config, template_manager):
        self.log = log
        self.template_manager = template_manager

        self.mount_point = config['project_mount_point']

        self.default_field_values = config['defaults']
        self.regexp_mapping = config['regexp_mapping']

        self.regexp_extractor = re.compile(
            '(?P<prefix>.+)?(\+)(?P<variable>.+)(\+)(?P<suffix>.+)?'
        )

    def build(self, name, data, path):
        ''' Build the given schema name, and replace data,
        level defines the depth of the built paths.

        :param name: The template *name* to build.
        :type name: str
        :param data: A set of data to fill the template with.
        :type name: dict
        :param path: the path where the structure has to be created.
        :type name: str
        '''
        current_path = path or self.mount_point
        current_path = os.path.realpath(current_path)

        self.log.debug('Building template : {0} in : {1}'.format(
            name, current_path)
        )

        if os.path.abspath(self.mount_point) not in os.path.abspath(current_path):
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
        # only if on posix , windows permissions are not handled
        if os.name == 'posix':
            for result in reversed(path_results):
                path = os.path.join(current_path, result['path'])
                permission = result['permission']
                permission = int(permission, 8)
                self.log.debug('Setting permission of {1} as {0}'.format(
                    oct(permission), os.path.realpath(path)
                ))
                try:
                    os.chmod(path, permission)
                except OSError, error:
                    self.log.debug(error)

        return path_results

    def parse(self, path, name):
        ''' Parse the provided path against
        the given schema name.

        :param path: The *path* to be parsed.
        :type path: str
        :param name: The teplate name to parse against.
        :type name: str

        '''
        # remove trailing slash from path
        if path.endswith(os.sep):
            path = path[:-1]

        if not path.startswith(self.mount_point):
            self.log.exception(
                ('The path %s does not seems contained'
                 ' in the given mount_point %s') % (
                    path, self.mount_point
                )
            )
            return []

        path = path.split(self.mount_point)[-1]
        if path.startswith(os.sep):
            path = path[1:]

        self.log.debug('Parsing {0} against {1}'.format(name, path))
        matched_results = []
        built = self.template_manager.resolve_template(name)
        results = self.template_manager.resolve(built)
        parsers = self._to_parser(results)

        for parser in parsers:
            self.log.debug('Creating parser : {0}'.format(parser))
            check = re.compile(parser)
            match = check.match(path)
            if not match:
                self.log.debug('no match found for {0} with {1}'.format(
                    path, parser
                ))
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
        return matched_results or []

    def _to_parser(self, paths):
        ''' Recursively build a parser from the
        given set of schema paths

        '''
        result_paths = []
        for path in paths:
            result_path = []
            path = path['path']
            for entry in path:
                matches = self.regexp_extractor.match(entry)
                if matches:
                    data = matches.groupdict()
                    prefix = data.get('prefix')
                    entry = data.get('variable')
                    suffix = data.get('suffix')
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

                    if prefix:
                        entry = prefix+entry

                    if suffix:
                        entry = entry+suffix

                result_path.append(entry)

            # Enforce checking with ^$
            # TODO: Protect slashes with backslashes in (os.sep*2).join...
            formatted_path = (os.sep).join(result_path)
            result_path = r'^{0}$'.format(formatted_path)
            self.log.debug('Building regex : {0}'.format(result_path))
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
                        'Key {1} for data {0} does not match {2}'.format(
                            name, value, self.regexp_mapping[name].keys()
                        )
                    )
                    data.pop(name)
            else:
                self.log.debug('Key %s not in %s' % (
                    name, self.regexp_mapping.keys())
                )

    def _set_default_values(self, data):
        self.log.debug('Updating data with defaults: {0}'.format(
            pformat(self.default_field_values)
            )
        )
        for key, val in self.default_field_values.items():
            data.setdefault(key, val)

    def _to_path(self, paths, data):
        ''' Recursively build a list of paths from the given
        set of schema paths.

        '''
        data = data or OrderedDict()
        self._set_default_values(data)
        self._validate_data(data)
        result_paths = []
        for entry in paths:
            result_path = []
            for item in entry['path']:
                matches = self.regexp_extractor.match(item)
                if matches:
                    match = matches.groupdict()
                    prefix = match.get('prefix')
                    item = match.get('variable')
                    suffix = match.get('suffix')

                    item = '{%s}' % item

                    if prefix:
                        item = prefix + item

                    if suffix:
                        item = item + suffix

                result_path.append(item)

            isnotinresults = result_path not in result_paths
            if isnotinresults:
                final_path = (os.sep).join(result_path)
                self.log.debug('Building path for %s and data %s' % (final_path, data.keys()))
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
            else:
                self.log.warning('{0} already in {1}'.format(
                    result_path, result_paths
                    ))

        return result_paths
