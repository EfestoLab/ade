import re
from pprint import pformat

from manager import StructureManager


if __name__ == '__main__':
	'''Function entry point'''

	M = StructureManager('./templates')
	schema = '@+show+@'

	print 'PARSERs:'
	pareser_results = M.to_parser(schema)
	print pformat(pareser_results)

	print 'PATHs:'
	context = {
		'show': 'white',
		'department': 'pipeline',
		'sequence': 'staging',
		'shot': 'src',
		'user': 'ennio',
		'python_version': '2.6.4'
	}

	path_results = M.to_path(schema, context)
	print pformat(path_results)

	print 'TEST:'
	for result in pareser_results:
		check = re.compile(result)
		match = check.match(path_results[16])
		if not match:
			continue

		print match.groupdict()
