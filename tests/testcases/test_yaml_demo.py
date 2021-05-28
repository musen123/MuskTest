"""
============================
Author:柠檬班-木森
Time:2021/3/1 20:20
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
=======
"""
from apin.core.httptest import HttpCase


class TestYamlDemo(HttpCase):
    host = "http://api.lemonban.com/futureloan/"
    headers = {
        "X-Lemonban-Media-Type": "lemonban.v2"
    }
    # 用例级别前置
    setup_hook = {
        "timestamp": 'F{get_timestamp()}'
    }
    # 类级别前置
    setup_class_hook = {
    }
    # 预设变量
    env = {
        "user_mobile": 'F{rand_phone("155")}',
        "admin_mobile": 'F{rand_phone("133")}'
    }
    # 提取变量
    extract = {
    }
    verification = [
        ["eq", {'code': 0, "msg": "OK"}, {'code': 'V{{$..code}}', "msg": "V{{$..msg}}"}]
    ]

    Cases = 'qcd.yaml'
