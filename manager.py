'''

'''
import os
import copy
from pprint import pformat


class StructureManager(object):
	'''Structure manager class,
	Provide standard methods to create virtual file structure
	from disk fragment

	'''
	def __init__(self, template_folder):
		self._register = {}
		self._template_folder = template_folder
		self.parse()

	def resolve(self, name):
		'''Return the resolved path of the given variable *name*'''
		clean_name = name.replace('@', '')
		entry = {clean_name: {}}

		self._resolve(
			self._register.get(name, {}),
			entry[clean_name]
		)

		return entry

	def _resolve(self, input, output):
		'''Recursively resolve the given *input* path into *output*'''
		for key, value in input.items():
			if isinstance(value, dict):

				if key.startswith('@'):
					path_fragment = self._register.get(key, {})
					fragment = {}
					self._resolve(path_fragment, fragment)
					output.setdefault(key.replace('@', ''), fragment)
				else:
					output.setdefault(key, {})
					self._resolve(value, output[key])
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
					default= None
				#stats = os.stat(subfolder)
				#print stats
				mapped.setdefault(folder, default)
				self._folder_map(subfolder, mapped[folder])


if __name__ == '__main__':
	M = StructureManager('./templates')

	show_result = M.resolve('@+show+@')
	# seq_result = M.resolve('@+sequence+@')
	# shot_result = M.resolve('@+shot+@')
	# nuke_result = M.resolve('@nuke@')

	print pformat(show_result)
	#print pformat(M._register)
