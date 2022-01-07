"""
============================
Project: Apin
Author:柠檬班-木森
Time:2021/8/11 20:25
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
Site: http://www.lemonban.com
Forum: http://testingpai.com 
============================
"""
from apin.core.tools import *
from hooks.db_check_hook import *
from hooks.fixture_hook import *


def rand_phone(st1):
    return random_mobile()


def get_sign(a,b):
    return get_timestamp()
