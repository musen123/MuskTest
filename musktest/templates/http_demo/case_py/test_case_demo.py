# Author:码思客-木森
# WeChart:musen9111

from musktest.core.httptest import HttpCase


class TestDome1(HttpCase):
    # host地址,如果setting中定义了此处可以不写
    host = "http://httpbin.org"
    # 请求头
    headers = {
        "UserAgent": "python/musktest"
    }
    # 请求方法
    method = 'get'
    # 接口地址
    interface = '/get'
    # 指定用例级别的前置钩子
    setup_hook = "setup_hook_demo"
    # 指定用例级别的猴子猴子
    teardown_hook = "teardown_hook_demo"
    # 用例断言
    verification = [
        ["eq", 200, "status_code"]
    ]
    # 用例数据
    Cases = [
        # 用例1
        {
            "title": "py文件-用例1",
            "json": {
                "mobile_phone": "17788907899",
                "pwd": "msktest"
            },
        },
        # 用例2
        {
            "title": "py文件-用例2",
            "json": {
                "mobile_phone": "17788907899",
                "pwd": "msktest"
            }
        }
    ]
