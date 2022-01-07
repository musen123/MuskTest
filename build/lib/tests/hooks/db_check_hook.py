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
import random,time

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
    """获取时间戳,保存为全局变量"""
    ENV.timestamp = time.time()

def register_db_check(test, db, ENV, env):
    # 前置sql
    sql = "SELECT count(*) as count FROM futureloan.member WHERE mobile_phone='{}';".format(env.user_mobile)
    s_count = db.qcd.execute(sql)['count']
    yield
    # 后置sql
    e_count = db.qcd.execute(sql)['count']
    # sql校验规则
    return [
        ['eq', s_count + 1, e_count]
    ]
