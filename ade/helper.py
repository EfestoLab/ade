import logging
import tempfile

tmp_log = tempfile.NamedTemporaryFile(
    prefix='efestolab.uk.ade.', suffix='.log', delete=False
)


def setup_custom_logger(name, level=logging.DEBUG, tmp_file=None):
    """ Helper logging function.
    """

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
    logger.info('ADE Log file : %s' % tmp_log.name)
    return logger
