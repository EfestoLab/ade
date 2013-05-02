from pprint import pformat
from manager import StructureManager


if __name__ == '__main__':
	'''Function entry point'''

	M = StructureManager()
	schema = '@+show+@'
	#print pformat(M._register)
	resolved = M.resolve_schema(schema)
	print pformat(resolved)
	exit()

	print 'PARSERs:'
	pareser_results = M.to_parser(schema)
	#print pformat(pareser_results)

	print 'PATHs:'
	context = {
		'show': 'white',
		'department': 'pipeline',
		'sequence': 'AA',
		'shot': 'AA000',
		'user': 'ennio',
		'python_version': '2.6.4'
	}

	path_results = M.to_path(schema, context)
	#print pformat(path_results)

	path = path_results[12]
	#print 'TEST PARSE:', path

	results = M.parse(path, schema)
	#print pformat(results[0])
	#print pformat(results)
