from pprint import pformat
from manager import StructureManager


if __name__ == '__main__':
	'''Function entry point'''

	M = StructureManager()
	schema = '@+show+@'
	# #print pformat(M._register)
	#resolved_schema = M.resolve_schema(schema)
	#resolved = M.resolve(resolved_schema)

	#print pformat(resolved_schema)
	#print pformat(resolved)

	# print 'PARSERs:'
	# pareser_results = M.to_parser(schema)
	# print pformat(pareser_results)

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
	print pformat(path_results)

	build = M.build(schema, context)
	# path = path_results[11]
	# print 'TEST PARSE:', path

	# results = M.parse(path, schema)
	# print pformat(results[0])
	# print pformat(results)
