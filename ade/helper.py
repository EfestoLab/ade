import os
import logging
import tempfile

tmpfile_args = dict(
    prefix='efestolab.uk.ade.',
    suffix='.log',
    delete=False
)

logs_env = os.getenv('EFESTO_LOGS')
if logs_env:
    tmpfile_args['dir'] = logs_env

tmp_log = tempfile.NamedTemporaryFile(**tmpfile_args)


def setup_custom_logger(name, level=logging.INFO, tmp_file=None):
    """ Helper logging function.
    """

    is_debug = os.getenv('EFESTO_DEBUG', '0')
    if is_debug != '0':
        level = logging.DEBUG

    formatter = logging.Formatter(
        fmt='[%(levelname)s] '
        '%(lineno)s @ %(name)s.%(funcName)s() - %(message)s'
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    tmp = tmp_file or tmp_log.name
    fhandler = logging.FileHandler(tmp)
    fhandler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(fhandler)
    logger.debug('ADE Log file : %s' % tmp_log.name)
    logger.debug('Registering log for %s' % name)
    return logger
