#!/usr/bin/env python

import os
import json
import logging
import argparse
from pprint import pformat

from manager import filesystem
from manager import config
from manager import template as template


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
        'action', choices=['create', 'parse'],
        help='Application action'
    )

    parser.add_argument(
        '--config_path',
        help='search path for config files',
        default=os.getenv('ADE_CONFIG_PATH')
    )

    parser.add_argument(
        '--mode',
        help='one of the mode provided through the config search path',
        default=os.getenv('ADE_MODE', 'default')
    )

    parser.add_argument(
        '--template',
        help='Specify template to use (has to exist in the template folder).',
        default='@+show+@',
        choices=[
            '@+show+@', '@+department+@', '@+sequence+@',
            '@+shot+@', '@sandbox@'
        ],
    )

    parser.add_argument(
        '--verbose',
        default='info',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        help='Log verbosity level.'
    )

    parser.add_argument(
        '--path',
        default=os.path.realpath('./'),
        help='Path to be parsed or created to'
    )

    parser.add_argument(
        '--data',
        nargs='*',
        default=[],
        help='Fragment variables (build action only)'
    )

    args = vars(parser.parse_args())
    return args


def run():
    """
    Main entry point of ade command line.

    """
    args = arguments()
    config_path = args.get('config_path')
    if not config_path:
        print 'Please define: $ADE_CONFIG_PATH'
        return
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

    logger.debug('Using data: {0}'.format(pformat(input_data)))

    path = args.get('path')
    # Get the mountpoint
    if not os.path.exists(path):
            logger.warning('Input path {0} does not exist.'.format(path))
            return

    config_mode = args.get('mode')
    logger.info('loading mode {0} '.format(config_mode))
    config_manager = config.ConfigManager(config_path)
    config_mode = config_manager.get(config_mode)

    template_search_path = os.path.expandvars(
        config_mode['template_search_path']
    )

    root_template = config_mode['root_template']

    # Create a new manager

    template_manager = template.TemplateManager(template_search_path)
    manager = filesystem.FileSystemManager(
        config_mode,
        template_manager
        )

    input_template = args.get('template')

    if args.get('action') == 'create':
        current_data = manager.parse(path, root_template)
        print current_data
        manager.build(input_template, input_data, path)

    if args.get('action') == 'parse':
        path = os.path.realpath(path)

        if not os.path.exists(path):
            logger.warning('{0} does not exist.'.format(path))
            return

        results = manager.parse(path, root_template)
        if results:
            print json.dumps(results[0])
        else:
            logger.info('No data found to parse from {0}'.format(path))

if __name__ == '__main__':
    run()

