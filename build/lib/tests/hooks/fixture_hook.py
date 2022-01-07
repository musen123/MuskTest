"""
============================
Project: Apin
Author:柠檬班-木森
Time:2021/7/9 16:44
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
Site: http://www.lemonban.com
Forum: http://testingpai.com 
============================
"""
import random
import time


def setup_hook1(test, ENV, env, db):
    """
    随机生成一个手机号码，保存为全局变量user_phone
    :param ENV: 全局变量
    :param env: 局部变量
    :return:
    """
    phone = ''
    for i in range(8):
        phone += str(random.randint(0, 9))
    env.user_phone = phone


def get_timestamp_hook(test, ENV, env, db):
    """获取时间戳,保存为局部变量"""
    env.timestamp = time.time()


def teardown_hook1(test, ENV, env, db, response):
    print('测试用例后置钩子')
    pass
