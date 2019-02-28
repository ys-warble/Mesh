import logging

from WarbleSimulation import settings


def get_logger(name):
    logging_level = settings.LOGGING_LEVEL

    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
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
