"""
Author:柠檬班-木森
Time:2021/3/12 14:25
E-mail:3247119728@qq.com
"""
import importlib

try:
    settings = importlib.import_module('settings')
except:
    from apin.templates.http_demo import settings

ENV = getattr(settings, 'ENV', {})


class ParserDB:
    pass
