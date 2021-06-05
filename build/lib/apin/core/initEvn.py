"""
============================
Author:柠檬班-木森
E-mail:3247119728@qq.com
=======
"""
import importlib
import os
import sys
from .logger import Logger

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

ENV = getattr(settings, 'ENV', {})
