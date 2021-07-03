"""
============================
Author:柠檬班-木森
Time:2021/5/25 20:16
E-mail:3247119728@qq.com
=======
"""
import os
from apin.core.initEvn import ENV
from apin.core.testRunner import TestRunner
from apin.core.generateCase import ParserDataToCase


def run_test(env_config, case_data,
             func_tools_path=None,
             no_report=False,
             filename="reports.html",
             report_dir=".",
             title='测试报告',
             tester='测试员',
             desc="项目测试生成的报告",
             templates=1,
             thread_count=1,
             rerun=0,
             interval=2,
             ):
    """
    :param env_config: 全局环境变量
    :param case_data: 测试套件数据
    :param func_tools: 工具函数模块路径
    :param filename: 报告文件名
    :param report_dir:报告文件的路径
    :param title:测试套件标题
    :param templates: 可以通过参数值1或者2，指定报告的样式模板，目前只有两个模板
    :param tester:测试者
    :param thread_count:运行线程数
    :param rerun:失败重运行次数
    :param interval:重运行间隔事件
    :return:
    """
    if func_tools_path:
        with open(func_tools_path, 'rb') as f1, open('funcTools.py', 'wb') as f2:
            f2.write(f1.read())
    ENV.update(env_config)
    suite = ParserDataToCase.parser_data_create_cases([case_data])
    runner = TestRunner(suite=suite,
                        filename=filename,
                        report_dir=report_dir,
                        title=title,
                        tester=tester,
                        desc=desc,
                        templates=templates,
                        no_report=no_report
                        )
    res = runner.run(thread_count=thread_count, rerun=rerun, interval=interval)
    if func_tools_path:
        os.remove('funcTools.py')
    return res


if __name__ == '__main__':
    from apin import run_test

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
            "token": ("env", "jsonpath", "$..json"),
            'member_id': ("env", "jsonpath", "$..data")
        },
        "verification": [
            ["eq", 200, "status_code"]
        ],
        "Cases": [
            {
                "title": "测试用例",
                "interface": "/post",
                "method": "post",
                "json": {
                    "mobile_phone": "${{user_mobile}}",
                    "pwd": "lemonban"
                },
                "extract": {
                    "token": ("env", "jsonpath", "$..json"),
                    'member_id': ("ENV", "jsonpath", "$..headers")
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
                },

            }
        ]
    }
    ENV = {}
    res = run_test(env_config=ENV,
                   case_data=case_data,
                   func_tools_path=r'C:\project\MSUnitTestReport\TestApi\tests\musenTools.py',
                   no_report=True)
    print(res)
