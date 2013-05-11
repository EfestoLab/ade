'''
Structure manager

Provide a convenient class to construct virtual file path mapping
from a folder containing fragments.

'''
import os
import stat
import re
import copy
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('TemplateManager')




class TemplateManager(object):
	''' Template manager class,
	Provide standard methods to create virtual file structure
	from disk fragments.

	'''
	def __init__(self, template_folder=None):
		''' Initialization function.

		'''
		self.__default_templates = './templates'

		if not template_folder:
			log.warning(
				'No template folder provided, using : {0}'.format(self.__default_templates)
			)

		self.__reference_indicator = '@'
		self.__variable_indicator = '+'

		self._register = []
		self._template_folder = template_folder or self.__default_templates
		self.register_templates()

	@property
	def register(self):
		''' Return the content of the class register.

		'''
		return self._register

	def resolve(self, schema):
		''' Resolve the given schema name and return all the entries.

		'''
		paths = []
		self._resolve(
			schema,
			paths
		)
		paths.reverse()
		return paths

	def _resolve(self, schema, final_path_list, path=None):
		''' Recursively build the final_path_list from schema.

		'''
		path = path or [
			schema.get('name').replace(
				self.__reference_indicator, ''
			)
		]
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

			log.debug('Adding {0}'.format(new_entry))
			path.pop()

	def _get_in_register(self, name):
		''' Return a copy of the given schema name in register.

		'''
		for item in self.register:
			if item.get('name') == name:
				item = copy.deepcopy(item)
				return item
				break
		return {}

	def resolve_template(self, name):
		''' Return the built schema fragment of the given variable *name*.

		'''
		root = self._get_in_register(name)
		# Start the recursive build of the *root* folder, using *entry*
		self._resolve_template(
			root,
		)
		return root

	def _resolve_template(self, schema):
		''' Recursively build the given *schema* schema into *output*.

		'''
		for index, entry in enumerate(schema.get('children', [])):
			item = entry.get('name', '')
			if item.startswith(self.__reference_indicator):
				removed = schema['children'].pop(index)
				fragment = self._get_in_register(removed['name'])
				schema['children'].insert(index, fragment)
				self._resolve_template(fragment)
			else:
				self._resolve_template(entry)

	def register_templates(self, template_folder=None):
		''' Parse template path and fill up the register table.

		'''
		template_folder = template_folder or self._template_folder
		# resolve the and list the content of the template path
		template_path = os.path.realpath(template_folder)
		templates = os.listdir(template_path)

		# For each template root, recursively walk the content,
		# and register the hierarcy path in form of dictionary
		for template in templates:
			current_template_path = os.path.join(template_path, template)
			permission = stat.S_IMODE(os.stat(current_template_path).st_mode)

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

		'''
		# If the root is a folder
		if os.path.isdir(root):

			# Collect the content
			entries = os.listdir(root)
			for entry in entries:
				if entry.startswith('.git'):
					continue

				subentry = os.path.join(root, entry)
				permission = stat.S_IMODE(os.stat(subentry).st_mode)

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
