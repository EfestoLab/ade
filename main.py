import sys
import argparse
from manager import StructureManager


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument
	'''Function entry point'''
	M = StructureManager('./templates')
	#print 'register: ', pformat(M.register)
	built = M.resolve_schema('@+show+@')
	#print 'built: ', pformat(built)
	results = M.resolve(built)

	pareser_results = M.to_parser(results)
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

	pareser_results = M.to_path(results, context)
	print 'PATHs:'
	for result in pareser_results:
		print '/'.join(result)
