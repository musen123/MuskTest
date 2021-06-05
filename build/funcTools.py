"""
============================
Author:柠檬班-木森
Time:2021/6/5 20:35
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
=======
"""
import random


def rand_phone(phone='177'):
    for i in range(8):
        phone += str(random.randint(0, 9))
    return str(phone)
