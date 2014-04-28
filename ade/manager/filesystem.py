'''
FileSystemManager manager

Construct and parse results of the teplate manager

'''
import os
import re
import logging
from pprint import pformat

from template import TemplateManager

# DEFAULT REGEX FOR COMMON FOLDER TYPES
# TODO: This should be moved to config

regexp_config = {
    'show': '(?P<show>[a-zA-Z0-9_]+)',
    'sequence': '(?P<sequence>[a-zA-Z0-9_]+)',
    'shot': '(?P<shot>[a-zA-Z0-9_]+)',
    'department': '(?P<department>[a-zA-Z0-9_]+)'
}


class FileSystemManager(object):
    ''' Return an instance of FileSystemManager.
    :param template_manager: An instance of the templateManager.
    :type template_manager: TemplateManager
    :param mount_point: the start position of the build path.
    :type mount_point: str
    '''

    def __init__(self, mount_point, template_manager=None):
        self.__default_path_regex = '(?P<{0}>[a-zA-Z0-9_]+)'
        self.log = logging.getLogger('ade')
        self.mount_point = mount_point
        self.template_manager = template_manager or TemplateManager()

    def build(self, name, data):
        ''' Build the given schema name, and replace data,
        level defines the depth of the built paths.

        :param name: The template *name* to build.
        :type name: str
        :param data: A set of data to create the template with.
        :type name: dict
        '''
        self.log.debug('Building template : {0}'.format(name))
        current_path = self.mount_point
        built = self.template_manager.resolve_template(name)
        results = self.template_manager.resolve(built)
        path_results = self._to_path(results, data)
        for result in path_results:
            path = os.path.join(current_path, result['path'])
            try:
                if result['folder']:
                    # Create the folder
                    self.log.debug('creating folder: {0}'.format(path))
                    os.makedirs(path)
                else:
                    self.log.debug('creating file: {0}'.format(path))
                    file_content = result['content']
                    with open(path, 'w') as file_data:
                        file_data.write(file_content)
            except (IOError, OSError) as error:
                self.log.debug('{0} already exist'.format(path))
                pass

        # Set permissions, using the reversed results
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

            self.log.debug('Checking {0} with {1}'.format(
                path, parser
            ))
            match = check.search(path)
            if not match:
                continue
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
                    # Get the custom regex or use the default one
                    parser = regexp_config.get(
                        entry,
                        self.__default_path_regex
                    )
                    entry = parser.format(entry)
                result_path.append(entry)
            result_path = '^{0}$'.format((os.sep).join(result_path))
            result_paths.append(result_path)

        result_paths.sort(key=len)
        result_paths.reverse()
        self.log.debug('building parser %s' % pformat(result_paths))
        return result_paths

    def _to_path(self, paths, data):
        ''' Recursively build a list of paths from the given
        set of schema paths.

        '''
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
                    self.log.warning(
                        'PATHSKIP: {1} not found for {0}'.format(
                            final_path,
                            error
                        )
                    )
                    continue

                entry['path'] = final_path
                result_paths.append(entry)

        return result_paths
