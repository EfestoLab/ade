#!/usr/bin/env python

import os
import json

try:
    import efesto_logger as logging
except:
    import logging

import argparse

from manager import filesystem
from manager import config
from manager import template as template
from ade.manager.exceptions import ConfigError


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
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    # Print the given arguments
    # logger.debug('Arguments: {0}'.format(pformat(args)))

    # Create a dictionary from the user's import data
    input_data = args.get('data', [''])
    input_data = dict(
        [datum.split('=') for datum in input_data if '=' in datum]
    )

    path = args.get('path')
    # Get the mountpoint
    if not os.path.exists(path):
            logger.warning('Input path {0} does not exist.'.format(path))
            return

    config_mode = args.get('mode')
    logger.info('loading mode {0} '.format(config_mode))
    config_manager = config.ConfigManager(config_path)
    if config_mode not in config_manager.modes:
        raise ConfigError('Mode {0} is not available'.format(config_mode))

    config_mode = config_manager.get(config_mode)

    root_template = config_mode['root_template']

    # Create a new manager

    template_manager = template.TemplateManager(config_mode)
    manager = filesystem.FileSystemManager(
        config_mode,
        template_manager
        )

    input_template = args.get('template')

    if args.get('action') == 'create':
        # current_data = manager.parse(path, root_template)
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

