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
	from disk fragment

	'''
	def __init__(self, template_folder):
		''' Initialization function'''
		self._register = {}
		self._template_folder = template_folder
		self.parse()

	@property
	def register(self):
		''' Return the content of the class register'''
		return self._register

	def resolve(self, schema):
		'''resolve the given schema name and return all the folders'''
		paths = []
		self._resolve(
			schema,
			paths
		)
		return paths

	def build(self, name):
		'''Return the buildd path of the given variable *name*'''
		root = self._register.get(name)
		if not root:
			raise KeyError('{0} not found in register.'.format(name))
		clean_name = name.replace('@', '')
		entry = {clean_name: {}}

		self._build(
			root,
			entry[clean_name]
		)

		return entry

	def _resolve(self, fragment, paths, path=None):
		''' Build the final paths from fragment '''
		path = path or []
		for name, item in fragment.items():
			path.append(name)

			if item and isinstance(item, dict):
				self._resolve(item, paths, path)
			else:
				cpath = path[:]
				paths.append(cpath)

			removed = path.pop()
			fragment.pop(removed, None)

	def _build(self, input, output):
		'''Recursively build the given *input* path into *output*'''
		for key, value in input.items():
			if isinstance(value, dict):
				if key.startswith('@'):
					path_fragment = self._register.get(key, {})
					fragment = {}
					self._build(path_fragment, fragment)
					output.setdefault(key.replace('@', ''), fragment)
				else:
					output.setdefault(key, {})
					self._build(value, output[key])
			else:
				output[key] = None

	def parse(self):
		'''Parse the given template path and fill up the register table'''
		template_path = os.path.realpath(self._template_folder)
		templates = os.listdir(template_path)

		for template in templates:
			current_template_map = {}
			current_template_path = os.path.join(template_path, template)

			self._folder_map(current_template_path, current_template_map)
			self._register.setdefault(template, current_template_map)

	def _folder_map(self, start_folder, mapped):
		''' Recursively fill up the given *mapped* object with the
		hierarchical content of *start_folder*

		'''
		basefolder = os.path.realpath(start_folder)
		if os.path.exists(basefolder) and os.path.isdir(basefolder):
			folders = os.listdir(basefolder)
			for folder in folders:
				subfolder = os.path.join(basefolder, folder)
				default = {}
				if os.path.isfile(subfolder):
					default = None
				#stats = os.stat(subfolder)
				#print stats
				mapped.setdefault(folder, default)
				self._folder_map(subfolder, mapped[folder])


if __name__ == '__main__':
	'''Function entrypoint'''
	M = StructureManager('./templates')

	show_result = M.build('@+show+@')
	#print 'fragment: ', pformat(show_result)
	result = M.resolve(show_result)
	print 'Result', pformat(result)

	# seq_result = M.build('@+sequence+@')
	# shot_result = M.build('@+shot+@')
	# nuke_result = M.build('@nuke@')
	# sandbox_result = M.build('@sandbox@')
	#print 'Schema', pformat(show_result)
	# #print pformat(shot_result)
	# print pformat(seq_result)
	# #print pformat(nuke_result)
	# print pformat(sandbox_result)
