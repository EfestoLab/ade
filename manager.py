'''
Structure manager

Provide a convenient class to construct virtual file path mapping
from a folder containing fragments.

'''
import os
import stat
import re
import copy
from pprint import pformat

# DEFAULT REGEX FOR COMMON FOLDER TYPES
regexp_config = {
	'show': '(?P<show>[a-zA-Z0-9_]+)',
	'sequence': '(?P<sequence>[a-zA-Z0-9_]+)',
	'shot': '(?P<shot>[a-zA-Z0-9_]+)',
	'department': '(?P<department>[a-z_]+)'
}


class StructureManager(object):
	'''Structure manager class,
	Provide standard methods to create virtual file structure
	from disk fragments.

	'''
	def __init__(self, template_folder=None):
		''' Initialization function.'''
		if not template_folder:
			print 'Using default ./templates folder'
		self.__default_path_regex = '(?P<{0}>[a-zA-Z0-9_]+)'

		self.__reference_indicator = '@'
		self.__variable_indicator = '+'
		self._register = []
		self._template_folder = template_folder or './templates'
		self.parse_templates()

	@property
	def register(self):
		''' Return the content of the class register.'''
		return self._register

	def build(self, name, data, level=100):
		built = self.resolve_schema(name)
		results = self.resolve(built)
		#print pformat(results)
		for result in results:
			path = os.path.realpath('/'.join(result['path']))
			#permission = result['permissions']
			try:
				print 'creating:', path
				os.makedirs(path)
			except:
				pass

	def parse(self, path, name):
		parsers = self.to_parser(name)
		results = []

		for parser in parsers:
			check = re.compile(parser)
			match = check.match(path)
			if not match:
				continue
			result = match.groupdict()
			if result and result not in results:
				results.append(result)

		results.sort()
		results.reverse()
		return results

	def to_parser(self, name):
		built = self.resolve_schema(name)
		results = self.resolve(built)
		parsers = self._to_parser(results)
		paths = []
		for result in parsers:
			paths.append('/'.join(result))
		return paths

	def to_path(self, name, data, limit=100):
		built = self.resolve_schema(name)
		results = self.resolve(built)
		paths = self._to_path(results, data, limit)
		paths_result = []
		for result in paths:
			paths_result.append('/'.join(result))
		return paths_result

	def _to_parser(self, paths):
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
			result_paths.append(result_path)
		return result_paths

	def _to_path(self, paths, data, limit=100):
		result_paths = []
		for path in paths:
			result_path = []
			path = path['path']
			for entry in path[:limit]:
				if '+' in entry:
					entry = entry.split('+')[1]
					entry = '{%s}' % entry
					entry = entry.format(**data)

				result_path.append(entry)

			if result_path not in result_paths:
				result_paths.append(result_path)

		return result_paths

	def resolve(self, schema):
		'''resolve the given schema name and return all the folders.'''
		paths = []
		self._resolve(
			schema,
			paths
		)
		paths.reverse()
		return paths

	def _resolve(self, schema, final_path_list, path=None):
		'''Recursively build the final_path_list from schema.'''
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

			final_path_list.append(
				{
					'path': current_path,
					'permissions': entry.get('permission')
				}
			)
			path.pop()


	def _get_in_register(self, name):
		for item in self.register:
			if item.get('name') == name:
				item = copy.deepcopy(item)
				return item
				break
		return {}

	def resolve_schema(self, name):
		'''Return the built schema fragment of the given variable *name*.'''
		root = self._get_in_register(name)
		# Start the recursive build of the *root* folder, using *entry*
		self._resolve_schema(
			root,
		)
		return root

	def _resolve_schema(self, schema):
		'''Recursively build the given *schema* schema into *output*.'''
		for index, entry in enumerate(schema.get('children', [])):
			item = entry.get('name', '')
			if item.startswith(self.__reference_indicator):
				removed = schema['children'].pop(index)
				fragment = self._get_in_register(removed['name'])
				self._resolve_schema(fragment)
				print 'Remplacing: {0} with {1}'.format(item, pformat(fragment))
				schema['children'].insert(index, fragment)
			else:
				self._resolve_schema(entry)
				
	def parse_templates(self, template_folder=None):
		'''Parse template path and fill up the register table.'''
		template_folder = template_folder or self._template_folder
		# resolve the and list the content of the template path
		template_path = os.path.realpath(template_folder)
		templates = os.listdir(template_path)

		# For each template root, recursively walk the content,
		# and register the hierarcy path in form of dictionary
		for template in templates:
			current_template_path = os.path.join(template_path, template)
			permission = oct(stat.S_IMODE(os.stat(current_template_path).st_mode))

			current_template_map = {
				'name': template,
				'children': [],
				'permission': permission
			}

			self._parse_templates(
				current_template_path,
				current_template_map['children']
			)

			self._register.append(current_template_map)

	def _parse_templates(self, root, mapped):
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
				# Convert to a common format the file/folder permissions
				permission = oct(stat.S_IMODE(os.stat(subentry).st_mode))
				# We got a file.
				item = {
					'name': entry,
					'permission': permission
				}

				if os.path.isdir(subentry):
					# Add the current entry
					item = {
						'name': entry,
						'children': [],
						'permission': permission,
					}

					# Continue searching in folder
					self._parse_templates(subentry, item['children'])

				mapped.append(item)
