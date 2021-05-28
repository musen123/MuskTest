"""
============================
Author:柠檬班-木森
Time:2021/5/25 20:16
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
=======
"""
import unittest

from apin import TestRunner
from apin.core.basecase import GenerateTest
from apin.core.httptest import HttpCase

"""
1、获取全局的配置

2、获取工具函数模块

3、获取用例数据

"""


# 测试环境配置
conf = {}
# 用例数据
case_data = {
  "host": "http://httpbin.org",
  "headers": {
    "X-Lemonban-Media-Type": "lemonban.v2"
  },
  "setup_hook": {
    "timestamp": "F{get_timestamp()}"
  },
  "setup_class_hook": {
  },
  "env": {
    "user_mobile": "F{rand_phone()}",
    "admin_mobile": "F{rand_phone()}"
  },
  "extract": {
  },
  "verification": [
    ["eq", 200, "status_code"]
  ],
  "Cases": [
    {
      "title": "json-demo-1",
      "interface": "/post",
      "method": "post",
      "json": {
        "mobile_phone": "${{user_mobile}}",
        "pwd": "lemonban"
      }
    },
    {
      "title": "json-demo-2",
      "interface": "/post",
      "method": "post",
      "json": {
        "mobile_phone": "${{admin_mobile}}",
        "pwd": "lemonban",
        "type": 0
      }
    }
  ]
}
cls = GenerateTest('Case', (HttpCase,), case_data)
suite = unittest.defaultTestLoader.loadTestsFromTestCase(cls)

runner = TestRunner(suite=suite,report_dir=r'C:\project\MSUnitTestReport\TestApi\apin\templates\http_demo\reports')
runner.run()


