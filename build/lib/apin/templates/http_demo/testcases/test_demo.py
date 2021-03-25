"""
============================
Author:柠檬班-木森
Time:2021/3/1 20:20
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
=======
"""
from apin.core.httptest import HttpCase


class TestDome(HttpCase):
    host = "http://httpbin.org"
    headers = {"X-Lemonban-Media-Type": "lemonban.v2"}
    # 用例级别前置
    setup_hook = {"timestamp": 'F{get_timestamp()}'}
    # 预设变量
    env = {
        "user_mobile": 'F{rand_phone()}',
        "admin_mobile": 'F{rand_phone()}'
    }
    # 结果校验
    verification = [
        ["eq", 200, 'status_code'],
    ]

    Cases = [
        # 用例1：普通用户注册
        {
            'title': "py_case_demo1",
            'interface': "/post",
            "method": "post",
            'json': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},

        },
        # 用例2：管理员注册
        {
            'title': "py_case_demo2",
            'interface': "/post",
            "method": "post",
            'json': {"mobile_phone": "${{admin_mobile}}", "pwd": "lemonban", "type": 0}
        }

    ]
