#!/usr/bin/env python

import os
import json
import logging
import argparse
from pprint import pformat

from manager import filesystem


def setup_custom_logger(name):
    """ Helper logging function.
    """
    formatter = logging.Formatter(fmt='[%(levelname)s][%(module)s] - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


def arguments():
    """ Arguments accepted by the application.
    """
    parser = argparse.ArgumentParser(prog='ade')

    parser.add_argument(
        'mode', choices=['create', 'parse'],
        help='Application mode'
    )

    parser.add_argument(
        '--mount_point', help='Mount point for build/parse operation',
        default='/tmp'
    )

    parser.add_argument(
        '--template',
        help='Specify template to use (has to exist in the template folder).',
        default='@+show+@',
        choices=['@+show+@', '@+department+@', '@+sequence+@', '@+shot+@', '@sandbox@'],
    )

    parser.add_argument(
        '--template_folder',
        help='Specify template folder to use, if not provided relies on default.'
    )

    parser.add_argument(
        '--verbose',
        default='info',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        help='Log verbosity level.'
    )

    parser.add_argument(
        '--path',
        default='./',
        help='Path to be parsed (parse mode only)'
    )

    parser.add_argument(
        '--data',
        nargs='*',
        default=[],
        help='Fragment variables (build mode only)'
    )

    args = vars(parser.parse_args())
    return args


def run():
    """
    Main entry point of ade command line.

    """
    args = arguments()

    # Setup logging
    level = getattr(logging, args.get('verbose').upper())
    logger = setup_custom_logger('ade')
    logger.setLevel(level)

    # Print the given arguments
    # logger.debug('Arguments: {0}'.format(pformat(args)))

    # Create a dictionary from the user's import data
    input_data = args.get('data', [''])
    input_data = dict(
        [datum.split('=') for datum in input_data if '=' in datum]
    )

    # Lookup for common show environment variables
    input_data.setdefault('show', os.getenv('SHOW') or 'staging')
    input_data.setdefault('department', os.getenv('DEPARTMENT') or 'pipeline')
    input_data.setdefault('sequence', os.getenv('SEQUENCE') or 'rnd')
    input_data.setdefault('shot', os.getenv('SHOT') or 'test')
    input_data.setdefault('user', os.getenv('USER'))
    logger.debug('Using data: {0}'.format(pformat(input_data)))

    path = args.get('path')
    # Get the mountpoint
    mount_point = args.get('mount_point')
    if not os.path.exists(mount_point):
        logger.warning('{0} does not exist.'.format(mount_point))
        return

    # Create a new manager
    manager = filesystem.FileSystemManager(
        mount_point,
        args.get('template_folder'),
        )

    template = args.get('template')

    if args.get('mode') == 'create':
        manager.build(template, input_data, path)

    if args.get('mode') == 'parse':
        path = os.path.realpath(path)

        if not os.path.exists(path):
            logger.warning('{0} does not exist.'.format(path))
            return

        results = manager.parse(path, template)
        if results:
            print json.dumps(results[0])
        else:
            logger.info('No data found to parse from {0}'.format(path))

if __name__ == '__main__':
    run()
