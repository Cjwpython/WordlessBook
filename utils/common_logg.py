# coding: utf-8
import logging
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"

COLORS = {
    'WARNING': GREEN,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):

    def __init__(self, fmt=None, datefmt=None, style='%'):
        if fmt is None:
            fmt = "[%(asctime)s][%(name)s] [%(levelname)s] (%(filename)s:%(funcName)s:%(lineno)d) %(message)s"
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        levelname = record.levelname
        message = str(record.msg)
        funcName = record.funcName
        if levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            message_color = COLOR_SEQ % (30 + COLORS[levelname]) + message + RESET_SEQ
            funcName_color = COLOR_SEQ % (30 + COLORS[levelname]) + funcName + RESET_SEQ
            record.levelname = levelname_color
            record.msg = message_color
            record.funcName = funcName_color
        return logging.Formatter.format(self, record)
