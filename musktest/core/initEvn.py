# Author: -木森
# WeChart: python771

import importlib
import os
import sys
from musktest.core.logger import Logger
from musktest.core.DBClient import DBClient

sys.path.append(os.getcwd())
sys.path.append(os.path.abspath('..'))
try:
    func_tools = importlib.import_module('funcTools')
except ModuleNotFoundError:
    from musktest.core import tools as func_tools


class Settings:
    LOG_FILE_PATH = None
    DEBUG = True
    DB = []
    ENV = {}
    THREAD_COUNT = 1


try:
    settings = importlib.import_module('settings')
except:
    settings = Settings

if settings.DEBUG:
    log = Logger(path=getattr(settings, 'LOG_FILE_PATH', None),
                 level='DEBUG')
else:
    log = Logger(path=getattr(settings, 'LOG_FILE_PATH', None),
                 level='INFO')


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

    def __getattr__(self, item):
        if item != '__name' and item != '_BaseEnv__name':
            return super().__getitem__(item)
        return super().__getattribute__(item)

    def __delattr__(self, item):
        if item != '__name' and item != '_BaseEnv__name':
            super().__delitem__(item)
        else:
            super().__delattr__()


ENV = BaseEnv('ENV')
ENV.update(getattr(settings, 'ENV', {}))
DB = DBClient(getattr(settings, 'DB', []))
