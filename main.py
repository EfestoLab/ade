#!/usr/bin/env python

import sys
import argparse
from pprint import pformat

from manager import TemplateManager


def arguments():
	parser = argparse.ArgumentParser(description='Description of your program')
	parser.add_argument('-f','--foo', help='Description for foo argument', required=True)
	parser.add_argument('-b','--bar', help='Description for bar argument', required=True)
	args = vars(parser.parse_args())
	return args

if __name__ == '__main__':
	args = arguments()
	print args
	#print parser
	# M = TemplateManager()

	# schema = '@+show+@'
	# context = {
	# 	'show': 'white',
	# 	'department': 'show',
	# 	'sequence': 'AA',
	# 	'shot': 'AA000',
	# 	'user': 'ennio',
	# 	'python_version': '2.6.4'
	# }
	# build = M.build(schema, context)

