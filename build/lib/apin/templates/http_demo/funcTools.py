"""
    apin中内置了一些常用生成数据和 数据加密的工具函数,在apin.core.tools中,默认全部
导入到该文件中了，如果你不需要，可以把下面from apin.core.tools import * 这行
代码注释掉。

    apin作者的建议：如果你编写的钩子函数比较多,你可以在项目创建一个hook目录，在
hooks目录中创建多个python文件来编写你的钩子函数,然后导入到本文件中,这样后期
管理钩子函数更方便。

本文件中为给大家自动各类钩子函数定义的Demo,使用时参照demo去定义，在钩子函数实现自己的需求即可。

"""
from apin.core.tools import *



# -----------------工具函数的定义Demo--------------------
# 自定义的工具函数，可以在用例文件中可以直接通过F{函数()}来调用,也可以根据需求钩子函数中调用。
def random_phone():
    """随机生产一个135开头的手机号"""
    import random
    phone = '130'
    for i in range(8):
        phone += str(random.randint(0, 9))
    return str(phone)


def md5_encrypt(data):
    """
    md5加密的工具函数
    :param data: 加密的数据
    :return:
    """
    from hashlib import md5
    new_md5 = md5()
    new_md5.update(data.encode(encoding='utf-8'))
    return new_md5.hexdigest()


# ----------------前后置钩子函数定义的demo----------------
# 前后置钩子函数在用例文件中可以通过apin预留的前后置字段去指定

def setup_hook_demo(test, ENV, env, db):
    """
    用例级别的前置猴子函数
    :param test: 用例对象
    :param ENV: 全局变量
    :param env: 局部变量
    :param db:数据库操作对象
    :return:None
    """
    pass


def teardown_hook_demo(test, ENV, env, db, response):
    """
    用例级别的后置的钩子函数
    :param test: 用例对象
    :param ENV: 全局变量
    :param env: 局部变量
    :param db:数据库操作对象
    :param response: 请求完接口的响应对象
    :return:None
    """
    pass


def setup_class_hook_demo(ENV, env, db):
    """
    测试集级别的前置的钩子函数
    :param ENV: 用来接收全局环境变量
    :param env: 用来接收全局环境变量
    :param db:数据库操作对象
    :return: None
    """
    pass


def teardown_class_hook_demo(ENV, env, db):
    """
    测试集级别的后置的钩子函数
    :param ENV: 用来接收全局环境变量
    :param env: 用来接收全局环境变量
    :param db:数据库操作对象
    :return: None
    """
    pass


# -----------------------数据库校验钩子函数定义的demo-------------------------------
# 在用例文件中可以通过db_check_hook去指定
def db_check_hook_demo(test, ENV, env, db):
    """
    数据库校验的钩子函数
    :param test: 用例对象
    :param ENV: 全局变量
    :param env: 局部变量
    :param db:数据库操作对象
    :return: 校验规则 [['eq','预期结果','实际结果']]
    yield之前写用例执行之前的sql
    yield之后写用例执行之后的sql

    Demo:
    def register_db_check(test, db, ENV, env):
        sql = "SELECT count(*) as count FROM user"
        # 前置sql查询
        s_count = db.qcd.execute(sql)['count']
        yield
        # 后置sql查询
        e_count = db.qcd.execute(sql)['count']
        # 返回sql校验表达式
        return [
            ['eq', 1, e_count-s_count]
        ]

    """
    yield
