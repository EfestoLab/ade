import logging
import tempfile


def setup_custom_logger(name, level=logging.INFO):
    """ Helper logging function.
    """

    formatter = logging.Formatter(
        fmt='[%(levelname)s] '
        '%(lineno)s @ %(name)s.%(funcName)s() - %(message)s'
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    tmp_log = tempfile.NamedTemporaryFile(
        prefix='efestolab.uk.ade.', suffix='.log', delete=False
    )
    fhandler = logging.FileHandler(tmp_log.name)
    fhandler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(fhandler)
    logger.info('ADE Log file : %s' % tmp_log.name)
    return logger
