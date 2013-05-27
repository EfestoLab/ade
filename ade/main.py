#!/usr/bin/env python

import os
import argparse
from pprint import pformat
import logging

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
        '--mount_point', help='Mount point for build/parse',
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
        help='Path to be parsed.'
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

    logger.debug('Arguments: {0}'.format(pformat(args)))

    manager = filesystem.FileSystemManager(args.get('template_folder'))
    context = {
        'show': 'white',
        'department': 'job',
        'sequence': 'AF',
        'shot':'AF001',
        'user': 'langeli'
    }
    mount_point = args.get('mount_point')
    template = args.get('template')

    if args.get('mode') == 'create':
        manager.build(template, context, root=mount_point)

    if args.get('mode') == 'parse':
        path = os.path.realpath(args.get('path'))
        relative_path = path.split(mount_point)[-1]

        if relative_path.startswith('/'):
            relative_path = relative_path[1:]

        results = manager.parse(relative_path, template)
        logger.info('Result: {0}'.format(pformat(results[0])))

if __name__ == '__main__':
    run()