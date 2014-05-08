'''
Structure manager

Provide a convenient class to construct virtual file path mapping
from a folder containing fragments.

'''
import os
import stat
import copy
import logging
from pprint import pformat

log = logging.getLogger('ade')


class TemplateManager(object):
    ''' Template manager class,
    Provide standard methods to create virtual file structure
    from disk fragments.

    :param template_folder: The path to the config folder.
    :type template_folder: str

    '''
    def __init__(self, config=None):
        ''' Initialization function.

        '''
        # current_path = os.path.dirname(os.path.abspath(__file__))
        self.__reference_indicator = '@'
        self.__variable_indicator = '+'

        self._register = []
        template_folder = config.get('template_search_path')
        self._template_folder = os.path.realpath(template_folder)
        log.debug('Using template path: {0}'.format(self._template_folder))
        self.register_templates()

    @property
    def register(self):
        ''' Return the templates registered.
        '''
        return self._register

    def resolve(self, schema):
        ''' Resolve the given *schema* data and return all the entries.

            :param schema: The schema to resolve.
            :type schema: dict
            :returns:  list -- the resolved paths.
            :raises: AttributeError, KeyError

            .. code-block:: python

                from ade.schema.template import TemplateManager

                manager = TemplateManager('./templates')
                schema = manager.resolve_template('@+show+@')
                resolved_schema = manager.resolve_template(schema)

        '''
        root_name = schema.get('name').replace(self.__reference_indicator, '')

        root = {
            'path': [root_name],
            'permission': schema.get('permission', 777),
            'folder': schema.get('folder', True),
            'content': schema.get('content', '')
        }

        paths = [root_name]

        result_paths = []
        self._resolve(
            schema,
            result_paths,
            paths
        )
        result_paths.append(root)
        result_paths.reverse()
        # paths.sort(key=lambda x: len(x['path']))
        return result_paths

    def _resolve(self, schema, final_path_list, path=None):
        ''' Recursively build the final_path_list from schema.

        :param schema: The *schema* informations
        :type name: str
        :param final_path_list: The resolved list of paths
        :type name: list
        :param path: An internal memory reference for the recursive function.
        :type name: list

        .. note::
            This function is meant to be called only from within
            the resolve function

        '''
        for index, entry in enumerate(schema.get('children', [])):
            name = entry.get('name')
            name = name.replace(self.__reference_indicator, '')
            path.append(name)
            current_path = path[:]
            self._resolve(entry, final_path_list, path)

            new_entry = {
                'path': current_path,
                'permission': entry.get('permission', 777),
                'folder': entry.get('folder', True),
                'content': entry.get('content', '')
            }

            final_path_list.append(
                new_entry
            )

            path.pop()

    def _get_in_register(self, name):
        ''' Return a copy of the given schema name in register.

            :param name: The template *name*.
            :type name: str
            :returns:  dict -- the found template.
            :raises: KeyError

            .. code-block:: python

                from ade.schema.template import TemplateManager
                from ade.schema.config import ConfigManager

                config_manager = ConfigManager('path/to/config')
                manager = TemplateManager(config_manager)
                schema = manager._get_in_register('@+show+@')

        '''
        for item in self.register:
            if not item.get('name') == name:
                continue
            item = copy.deepcopy(item)
            return item

        raise KeyError('{0} not found in register'.format(name))

    def resolve_template(self, name):
        ''' Return the built schema fragment of the given variable *name*.

            :param name: The template *name*.
            :type name: str
            :returns:  dict -- the resolved template.
            :raises: AttributeError, KeyError

            .. code-block:: python

                from ade.schema.template import TemplateManager
                from ade.schema.config import ConfigManager

                config_manager = ConfigManager('path/to/config')
                manager = TemplateManager(config_manager)
                schema = manager.resolve_template('@+show+@')

        '''
        root = self._get_in_register(name)
        self._resolve_template(
            root,
        )
        return root

    def _resolve_template(self, schema):
        ''' Recursively resolve in place the given *schema* schema.

        :param name: The *schema* template to be resolved.
        :type name: dict

        .. note::
            This function is meant to be called only from within
            the resolve_template function.

        '''
        for index, entry in enumerate(schema.get('children', [])):
            item = entry.get('name', '')
            if item.startswith(self.__reference_indicator):
                removed = schema['children'].pop(index)
                fragment = self._get_in_register(removed['name'])
                if removed.get('children'):
                    fragment['children'].extend(removed['children'])

                schema['children'].insert(index, fragment)
                self._resolve_template(fragment)
            else:
                self._resolve_template(entry)

    def register_templates(self, template_folder=None):
        ''' Parse template path and fill up the register table.

            :param template_folder: The template path.
            :type template_folder: str

            .. code-block:: python

                from ade.schema.template import TemplateManager

                manager = TemplateManager()
                manager.register_templates('some/path/to/template')
        '''
        template_folder = template_folder or self._template_folder
        template_path = os.path.realpath(template_folder)
        templates = os.listdir(template_path)

        # For each template root, recursively walk the content,
        # and register the hierarcy path in form of dictionary
        for template in templates:
            current_template_path = os.path.join(template_path, template)
            permission = oct(stat.S_IMODE(
                os.stat(current_template_path).st_mode
            ))

            current_template_map = {
                'name': template,
                'children': [],
                'permission': permission,
                'folder': True
            }

            self._register_templates(
                current_template_path,
                current_template_map['children']
            )

            self._register.append(current_template_map)

    def _register_templates(self, root, mapped):
        ''' Recursively fill up the given *mapped* object with the
        hierarchical content of *root*.

        :param root: The root path.
        :type root: str

        :param mapped: The destination mapping.
        :type mapped: dict

        .. note::
            This recursive function is meant to be called only
            from within the register_template function

        '''
        # If the root is a folder
        if os.path.isdir(root):

            # Collect the content
            entries = os.listdir(root)
            for entry in entries:
                if entry.startswith('.git'):
                    continue

                subentry = os.path.join(root, entry)
                permission = oct(stat.S_IMODE(os.stat(subentry).st_mode))

                item = {
                    'name': entry,
                    'permission': permission,
                    'folder': False
                }

                if os.path.isdir(subentry):
                    # If it's a folder, mark it with children and type
                    item['children'] = []
                    item['folder'] = True

                    # Continue searching in folder
                    self._register_templates(subentry, item['children'])
                else:
                    # If it's a file store the content
                    item['content'] = open(subentry, 'r').read()

                mapped.append(item)
