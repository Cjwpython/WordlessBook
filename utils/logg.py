config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s][%(name)s] [**%(levelname)s**] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s',
        },
        "color": {
            "()": "utils.common_logg.ColoredFormatter",
            "format": "[%(asctime)s][%(name)s] [**%(levelname)s**] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': "color"
        }
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
if __name__ == '__main__':
    import logging.config

    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')
