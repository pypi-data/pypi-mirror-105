import logging


def init_logger(file_path: str,
                level: str = 'info',
                fmt: str = '',
                datefmt: str = '') -> None:
    levels = {'critical': logging.CRITICAL,
              'error': logging.ERROR,
              'warning': logging.WARNING,
              'info': logging.INFO,
              'debug': logging.DEBUG,
              'notset': logging.NOTSET}
    try:
        level = levels[level]
    except KeyError:
        print(f'Invalid level selection of {level}, using "info".')
        level = levels['info']
    handler = logging.FileHandler(file_path)
    if not fmt:
        fmt = '%(asctime)s:: %(levelname)s:: %(message)s'
    if not datefmt:
        datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt, datefmt)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    #handler.setStream(stream = None)
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    logger.addHandler(handler)

def mlog(message: str, level: str = 'info') -> None:
    logger = logging.getLogger(__name__)
    message = str(message)
    levels = {'critical': logger.critical,
              'error': logger.error,
              'warning': logger.warning,
              'info': logger.info,
              'debug': logger.debug}
    try:
        levels[level](message)
    except (KeyError, ValueError):
        print(f'Invalid level selection of {level}, using "info".')
        levels['info'](message)
