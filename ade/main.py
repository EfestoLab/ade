#!/usr/bin/env python

import os
import argparse
from pprint import pformat
import logging

from manager import filesystem


def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='[%(levelname)s][%(module)s] - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


def arguments():
    parser = argparse.ArgumentParser(prog='ade')

    parser.add_argument('mode', choices=['build', 'parse'],
                        help='Mode of the application')

    parser.add_argument('--mount_point',
                        help='Mount point for build/parse')

    parser.add_argument(
        '--verbosity',
        default='info',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        help='Logging output verbosity.'
    )

    args = vars(parser.parse_args())
    return args


def run():
    args = arguments()
    #print 'ARGS', args
    level = getattr(logging, args.get('verbosity').upper())
    logger = setup_custom_logger('ade')
    logger.setLevel(level)

    M = filesystem.FileSystemManager()

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