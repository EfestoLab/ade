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
from pprint import pformat

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('TemplateManager')


# DEFAULT REGEX FOR COMMON FOLDER TYPES
regexp_config = {
	'show': '(?P<show>[a-zA-Z0-9_]+)',
	'sequence': '(?P<sequence>[a-zA-Z0-9_]+)',
	'shot': '(?P<shot>[a-zA-Z0-9_]+)',
	'department': '(?P<department>[a-z_]+)'
}


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

		self.__default_path_regex = '(?P<{0}>[a-zA-Z0-9_]+)'
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

	def build(self, name, data, level=100):
		''' Build the given schema name, and replace data, 
		level defines the depth of the built paths.
		
		'''

		built = self.resolve_template(name)
		results = self.resolve(built)
		path_results = self._to_path(results, data, 1000)
		
		# Create folder
		for result in path_results:
			path = os.path.realpath(result['path'])
			if result['folder']:
				# Create the folder
				log.info('creating folder: {0}'.format(path))
				try:
					os.makedirs(path)
				except Exception, error:
					log.warning(error)
					pass
			else:
				# Create file
				log.info('creating file: {0}'.format(path))
				try:
					f = open(path, 'w')
				except IOError, error:
					log.warning(error)
					pass
				
		# Set permissions, using the reversed results
		for result in reversed(path_results):
			path = result['path']
			permission = int(result['permission'])

			log.info('setting {0} for {1}'.format(permission, path))
			try:
				os.chmod(path, permission)
			except OSError, error:
				log.warning(error)

	def parse(self, path, name):
		''' Parse the provided path against 
		the given schema name.

		'''
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
		''' Convert a schema name to a set of parser regex.

		'''
		built = self.resolve_template(name)
		results = self.resolve(built)
		parsers = self._to_parser(results)
		paths = []
		for result in parsers:
			paths.append('/'.join(result))
		return paths

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
			result_paths.append(result_path)
		return result_paths

	def _to_path(self, paths, data, limit=100):
		''' Recursively build a list of paths from the given
		 set of schema paths.

		 '''
		result_paths = []
		for entry in paths:
			result_path = []
			for item in entry['path'][:limit]:
			 	if '+' in item:
			 		item = item.split('+')[1]
			 		item = '{%s}' % item
			 	result_path.append(item)	

			if result_path not in result_paths:
				final_path = (os.sep).join(result_path)
				final_path = final_path.format(**data)
				entry['path'] = final_path
		 		result_paths.append(entry)

		return result_paths 

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
				'folder': entry.get('folder', True)
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
			permission = oct(stat.S_IMODE(os.stat(current_template_path).st_mode))

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
				# Convert to a common format the file/folder permissions
				permission = oct(stat.S_IMODE(os.stat(subentry).st_mode))
				# We got a file.
				item = {
					'name': entry,
					'permission': permission,
					'folder': False
				}

				if os.path.isdir(subentry):
					# Add the current entry
					item['children'] = []
					item['folder'] = True

					# Continue searching in folder
					self._register_templates(subentry, item['children'])

				mapped.append(item)
