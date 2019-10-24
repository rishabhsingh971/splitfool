import logging


def get_logger(level=logging.DEBUG):
    logger = logging.getLogger('splitfool')
    logger.setLevel(level)
    logger.removeHandler
    if not logger.hasHandlers():
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
        )
        # console handler
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
