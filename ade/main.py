#!/usr/bin/env python

import os
import argparse
from pprint import pformat

from ade.manager.filesystem import FileSystemManager


def arguments():
    parser = argparse.ArgumentParser(prog='ade')
    parser.add_argument('--version', action='store_true')
    parser.add_argument('--verbose', action='store_true')

    subparsers = parser.add_subparsers()
    parser_a = subparsers.add_parser('create')
    parser_a.add_argument('--destination_path', type=str)
    parser_a.add_argument('--template_name', type=str)

    parser_b = subparsers.add_parser('parse')
    parser_b.add_argument('--target_path', type=str)
    parser_b.add_argument('--mount_point', type=str)

    args = vars(parser.parse_args())
    return args

def run():
    args = arguments()
    print 'ARGS', args

    M = FileSystemManager()

    schema = '@+show+@'
    context = {
        'show': 'white',
        'department': 'job',
        'sequence': 'AF',
        'shot':'AF001',
        'user': 'langeli'
    }

    current_path = os.path.realpath('./_tmp_')
    M.build(schema, context, root=current_path)
    path = 'white/dev/AA/AA000/sandbox/ennio'
    results = M.parse(path, schema)
    print pformat(results[0])

if __name__ == '__main__':
    run()