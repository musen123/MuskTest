# Author:柠檬班-木森
# E-mail:musen_nmb@qq.com

import importlib
import os
import sys
from apin.core.logger import Logger

sys.path.append(os.getcwd())
sys.path.append(os.path.abspath('..'))
try:
    func_tools = importlib.import_module('funcTools')
except ModuleNotFoundError:
    from apin.core import tools as func_tools


class Settings:
    LOG_FILE_PATH = None
    DEBUG = True
    DB = {}
    ENV = {}
    THREAD_COUNT = 1


try:
    settings = importlib.import_module('settings')
except:
    settings = Settings

log = Logger(path=getattr(settings, 'LOG_FILE_PATH', None),
             level=getattr(settings, 'LOG_FILE_PATH', 'DEBUG'))


class BaseEnv(dict):

    def __init__(self, name, **kwargs):
        self.__name = name
        super().__init__(**kwargs)

    def __setitem__(self, key, value):
        if self.__name == 'ENV':
            log.debug('设置全局变量:\n{:<10}: {}'.format(key, value))
        else:
            log.debug('设置局部变量:\n{:<10}: {}'.format(key, value))
        super().__setitem__(key, value)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key != '__name' and key != '_BaseEnv__name':
            self.__setitem__(key, value)


ENV = BaseEnv('ENV')
ENV.update(getattr(settings, 'ENV', {}))
