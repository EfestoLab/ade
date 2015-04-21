import logging


def setup_custom_logger(name):
    """ Helper logging function.
    """
    formatter = logging.Formatter(
        fmt='[%(levelname)s][%(module)s] - %(message)s'
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    fhandler = logging.FileHandler('ade.log')
    fhandler.setLevel(logging.DEBUG)
    fhandler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(fhandler)
    return logger
