import logging

from WarbleSimulation import settings

logger = None

DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def get_logger(name):
    # create logger
    global logger
    if logger is None or logger.name != name:
        logger = logging.getLogger(name)

        logging_level = settings.LOGGING_LEVEL
        logger.setLevel(logging_level)
        logger.handlers = []

        if settings.LOGGING_CONSOLE is True:
            ch = logging.StreamHandler()
            ch.setLevel(settings.LOGGING_CONSOLE_LEVEL if settings.LOGGING_CONSOLE_LEVEL is not None else logging_level)
            ch.setFormatter(logging.Formatter(
                settings.LOGGING_CONSOLE_FORMAT if settings.LOGGING_CONSOLE_FORMAT is not None else DEFAULT_FORMAT))
            logger.addHandler(ch)

        if settings.LOGGING_FILE is True:
            ch = logging.FileHandler(
                settings.LOGGING_FILE_NAME if settings.LOGGING_FILE_NAME is not None else 'run.log')
            ch.setLevel(settings.LOGGING_FILE_LEVEL if settings.LOGGING_FILE_LEVEL is not None else logging_level)
            ch.setFormatter(logging.Formatter(
                settings.LOGGING_FILE_FORMAT if settings.LOGGING_FILE_FORMAT is not None else DEFAULT_FORMAT))
            logger.addHandler(ch)

    return logger


if __name__ == '__main__':
    theLogger = get_logger('simple_example')
    # 'application' code
    theLogger.debug('debug message')
    theLogger.info('info message')
    theLogger.warning('warn message')
    theLogger.error('error message')
    theLogger.critical('critical message')
