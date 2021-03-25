"""
============================
Author:柠檬班-木森
Time:2021/3/1 20:20
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
=======
"""
from apin.core.httptest import HttpCase


class TestDomeV3(HttpCase):
    host = "http://api.lemonban.com/futureloan/"
    headers = {"X-Lemonban-Media-Type": "lemonban.v2"}
    # 用例级别前置
    setup_hook = {"timestamp": 'F{get_timestamp()}'}
    # 预设变量
    env = {
        "user_mobile": 'F{rand_phone("155")}',
        "admin_mobile": 'F{rand_phone("133")}'
    }
    # 结果校验
    verification = [
        ["eq", 200, 'status_code'],
        # {"method": "eq", "expected": {'code': 0, "msg": "OK"}, "actual": {'code': 'V{{$..code}}', "msg": "V{{$..msg}}"}}
        ["eq", {'code': 0, "msg": "OK"}, {'code': 'V{{$..code}}', "msg": "V{{$..msg}}"}]
    ]

    Cases = [
        # 用例1：普通用户注册
        {
            'title': "普通用户注册",
            'interface': "member/register",
            "method": "post",
            'json': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},

        },
        # 用例2：管理员注册
        {
            'title': "管理员注册",
            'interface': "member/register",
            "method": "post",
            'json': {"mobile_phone": "${{admin_mobile}}", "pwd": "lemonban", "type": 0}
        },
        # 用例3：普通用户登录
        {
            'title': "普通用户登录",
            'interface': "member/login",
            "method": "post",
            'json': {"mobile_phone": "${{user_mobile}}", "pwd": "lemonban"},
            "extract": {
                "token": ("env", "jsonpath", "$..token"),
                'member_id': ("env", "jsonpath", "$..id")
            }
        },
        # 用例4：充值
        {
            'title': "充值",
            'interface': "member/recharge",
            "method": "post",
            "headers": {
                "X-Lemonban-Media-Type": "lemonban.v2",
                "Authorization": "Bearer ${{token}}"
            },

            'json': {
                "member_id": '${{member_id}}',
                "amount": 20000,
                "timestamp": "${{timestamp}}",
                "sign": "F{get_sign(${{timestamp}},${{token}})}"
            }
        },
        # 用例5：管理员登录
        {
            'title': "管理员用户登录",
            'interface': "member/login",
            "method": "post",
            'json': {"mobile_phone": "${{admin_mobile}}", "pwd": "lemonban"},
            "extract": {
                "admin_token": ("env", "jsonpath", "$..token"),
                'admin_member_id': ("env", "jsonpath", "$..id")
            }
        },
        # 用例6：管理员添加项目
        {
            'title': "管理员添加项目",
            'interface': "loan/add",
            "method": "post",
            "timestamp": "F{get_timestamp()}",
            'json': {
                "member_id": '${{admin_member_id}}',
                "title": "世界这么大，借钱去看看",
                "amount": 2000.00,
                "loan_rate": 18.0,
                "loan_term": 6,
                "loan_date_type": 1,
                "bidding_days": 10,
                "timestamp": "${{timestamp}}",
                "sign": "F{get_sign(${{timestamp}},${{admin_token}})}"
            },
            "headers": {
                "X-Lemonban-Media-Type": "lemonban.v2",
                "Authorization": "Bearer ${{admin_token}}"
            },
            "extract": {
                'loan_id': ("env", "jsonpath", "$..id")
            }
        },
        # 用例7：管理员审核项目
        {
            'title': "管理员审核项目",
            'interface': "loan/audit",
            "method": "patch",
            "headers": {
                "X-Lemonban-Media-Type": "lemonban.v2",
                "Authorization": "Bearer ${{admin_token}}"
            },

            'json': {
                "loan_id": '${{loan_id}}',
                "approved_or_not": True,
                "timestamp": "${{timestamp}}",
                "sign": "F{get_sign(${{timestamp}},${{admin_token}})}"

            },
        },
        # 用例8：普通用户投资
        {
            'title': "普通用户投资",
            'interface': "member/recharge",
            "method": "post",
            "headers": {
                "X-Lemonban-Media-Type": "lemonban.v2",
                "Authorization": "Bearer ${{token}}"
            },

            'json': {
                "member_id": '${{member_id}}',
                "loan_id": '${{loan_id}}',
                "amount": 200,
                "timestamp": "${{timestamp}}",
                "sign": "F{get_sign(${{timestamp}},${{token}})}"
            }
        },
        # 用例9：取现
        {
            'title': "取现",
            'interface': "member/withdraw",
            "method": "post",
            "headers": {
                "X-Lemonban-Media-Type": "lemonban.v2",
                "Authorization": "Bearer ${{token}}"
            },
            'json': {
                "member_id": '${{member_id}}',
                "amount": 2000,
                "timestamp": "${{timestamp}}",
                "sign": "F{get_sign(${{timestamp}},${{token}})}"
            },
        }
    ]
