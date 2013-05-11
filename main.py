#!/usr/bin/env python

import os
import argparse
from pprint import pformat

from manager.filesystem import FileSystemManager


def arguments():
    parser = argparse.ArgumentParser(
        description='Command line for file system manager')
    parser.add_argument('-tp', '--templates_path', help='Templates folder path')
    parser.add_argument('-cp', '--current_path', help='Path to be checked')
    parser.add_argument('-bn', '--build_path', help='Template name to be used')
    parser.add_argument('-pp', '--parse_path', help='Parse the current path against the given template')

    args = vars(parser.parse_args())
    return args

if __name__ == '__main__':
    args = arguments()
    print 'ARGS', args

    M = FileSystemManager()

    schema = '@+show+@'
    context = {
        'show': 'white',
        'department': 'show',
        'sequence': 'AA',
        'shot': 'AA000',
    }

    current_path = os.path.realpath('./')
    build = M.build(schema, context, path=current_path)
    path = 'white/show/AA/AA000/sandbox/ennio'
    results = M.parse(path, schema)
    print pformat(results[0])
