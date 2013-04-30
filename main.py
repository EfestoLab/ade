import re
import argparse
from manager import StructureManager


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument
	'''Function entry point'''

	M = StructureManager('./templates')
	schema = '@+show+@'

	pareser_results = M.to_parser(schema)
	print 'PARSERs:'
	for result in pareser_results:
		print '/'.join(result)

	context = {
		'show': 'white',
		'department': 'pipeline',
		'sequence': 'staging',
		'shot': 'src',
		'user': 'ennio',
		'python_version': '2.6.4'
	}

	path_results = M.to_path(schema, context)
	print 'PATHs:'
	for result in path_results:
		print '/'.join(result)

	print 'TEST:'
	for result in pareser_results:
		regex = '/'.join(result)
		check = re.compile(regex)
		match = check.match('/'.join(path_results[4]))

		if not match:
			continue

		print match.groupdict()

