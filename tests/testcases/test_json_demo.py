from apin.core.httptest import HttpCase


class TestCeiKai(HttpCase):
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
    # j结果校验
    verification = [
        ["eq", 0, 'V{{$..code}}'],
        ["eq", "OK"]
    ]

    Cases = 'cekai.json'
