'''
Structure manager 

Provide a convenient class to construct virtual file path mapping
from a folder containing fragments.

'''

import os
from pprint import pformat


class StructureManager(object):
	'''Structure manager class,
	Provide standard methods to create virtual file structure
	from disk fragments.

	'''
	def __init__(self, template_folder):
		''' Initialization function.'''
		self.__reference_indicator = '@'
		self.__variable_indicator = '+'
		self._register = {}
		self._template_folder = template_folder
		self.parse_templates()

	@property
	def register(self):
		''' Return the content of the class register.'''
		return self._register

	def resolve_schema(self, schema):
		'''resolve the given schema name and return all the folders.'''
		paths = []
		self._resolve_schema(
			schema,
			paths
		)
		return paths

	def _resolve_schema(self, schema, final_path_list, path=None):
		'''Recursively build the final_path_list from schema.'''
		path = path or []
		for schema_name, schema_fragment in schema.items():
			# Add schema_name to path
			path.append(schema_name)

			# If the fragment exists and it's a compatible type, resolve it,
			# otherwise, add the path to the final path list (we reached a leaf)
			if schema_fragment and isinstance(schema_fragment, dict):
				self._resolve_schema(schema_fragment, final_path_list, path)
			else:
				current_path = path[:]
				final_path_list.append(current_path)

			# Remove the previously visited path entry
			path.pop()

	def build_schema(self, name):
		'''Return the built schema path of the given variable *name*.'''
		# Check if the given schema *name* exists
		root = self.register.get(name)
		if not root:
			raise KeyError('{0} not found in register.'.format(name))

		# Remove the reference indicator from the folder *name*
		clean_name = name.replace(self.__reference_indicator, '')

		# Build the first level of the schema
		entry = {clean_name: {}}

		# Start the recursive build of the *root* folder, using *entry*
		self._build_schema(
			root,
			entry[clean_name]
		)

		return entry

	def _build_schema(self, schema, output):
		'''Recursively build the given *schema* schema into *output*.'''
		for item_name, item_value in schema.items():

			# If the item is a reference to another path fragment,
			# Resolve it
			if item_name.startswith(self.__reference_indicator,):

				# Search the given fragment path
				fragment_path = self.register.get(item_name, {})

				# Build the given fragment into data
				data = {}
				self._build_schema(fragment_path, data)

				# Insert the resolved path fragment instead of the variable
				output.setdefault(
					item_name.replace(self.__reference_indicator, ''),
					data
				)
			else:
				# Insert the path fragment name and continue the build
				output.setdefault(item_name, {})
				self._build_schema(item_value, output[item_name])

	def parse_templates(self):
		'''Parse template path and fill up the register table.'''
		# resolve_schema the and list the content of the template path
		template_path = os.path.realpath(self._template_folder)
		templates = os.listdir(template_path)

		# For each template root, recursively walk the content,
		# and register the hierarcy path in form of dictionary
		for template in templates:
			current_template_map = {}
			current_template_path = os.path.join(template_path, template)
			self._parse_templates(current_template_path, current_template_map)
			self._register.setdefault(template, current_template_map)

	def _parse_templates(self, root, mapped):
		''' Recursively fill up the given *mapped* object with the
		hierarchical content of *root*.

		'''
		# If the root is a folder
		if os.path.isdir(root):

			# Collect the content
			folders = os.listdir(root)
			for folder in folders:

				# Add the current folder
				mapped.setdefault(folder, {})

				# Continue searching in folder
				subfolder = os.path.join(root, folder)
				self._parse_templates(subfolder, mapped[folder])

if __name__ == '__main__':
	'''Function entry point'''
	M = StructureManager('./templates')
	#print 'register: ', pformat(M.register)
	built = M.build_schema('@+shot+@')
	#print 'built: ', pformat(built)
	result = M.resolve_schema(built)
	print 'Result', pformat(result)
