'''

'''
import os
import copy
from pprint import pformat


class StructureManager(object):

	def __init__(self, template_folder):
		self._register = {}
		self._template_folder = template_folder
		self.parse()

	def resolve(self, name):
		clean_name = name.replace('@', '')
		entry = {clean_name: {}}
		self._resolve(self._register.get(name, {}), entry[clean_name])
		return entry

	def _resolve(self, input, output):
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

	def parse(self):
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
				mapped.setdefault(folder, {})
				newfolder = os.path.join(basefolder, folder)
				self._folder_map(newfolder, mapped[folder])


if __name__ == '__main__':
	M = StructureManager('./templates')
	show_result = M.resolve('@+show+@')
	seq_result = M.resolve('@+sequence+@')
	shot_result = M.resolve('@+shot+@')
	nuke_result = M.resolve('@nuke@')
