#!/usr/bin/env python

import sys
import argparse
from pprint import pformat

from template_manager import TemplateManager


def arguments():
	parser = argparse.ArgumentParser(description='Description of your program')
	parser.add_argument('-f','--foo', help='Description for foo argument')
	parser.add_argument('-b','--bar', help='Description for bar argument')
	args = vars(parser.parse_args())
	return args

if __name__ == '__main__':
	args = arguments()
	print 'ARGS', args

	M = TemplateManager()

	schema = '@+show+@'
	context = {
		'show': 'white',
		'department': 'show',
		'sequence': 'AA',
		'shot': 'AA000',
		'user': 'ennio',
		'python_version': '2.6.4'
	}

	build = M.build(schema, context)
	path = 'white/show/AA/AA000/sandbox/ennio'
	results = M.parse(path, schema)
	print pformat(results[0])
