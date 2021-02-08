# coding: utf-8
"""
加载app配置
路由注册
"""
import os
import sys
from flask import Flask
from config.base import BASEDIR
import logging.config
from utils.logg import config
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


class Application(Flask):
    """扩展插件类"""

    def __init__(self, import_name):
        super(Application, self).__init__(import_name, )
        env = os.environ.get('PROJECT_ENV')
        if not env:
            env = "local"
            logger.warning("load default config")
        if not os.path.exists(f"{BASEDIR}/config/{env}.py"):
            logger.error(f"configfile do not exist")
            sys.exit()
        self.config.from_pyfile(f"{BASEDIR}/config/{env}.py")


app = Application(__name__)

from .setting import *
