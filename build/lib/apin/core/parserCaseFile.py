"""
============================
Author:柠檬班-木森
Time:2021/3/15 15:08
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
=======
"""
import json
import os
import yaml
from apin.core.httptest import HttpCase
from apin.core.basecase import GenerateTest

import unittest


def parser_json_create_cases(dir: str):
    """解析json文件创建用例"""
    # 支持yaml

    files = os.listdir(dir)
    for filename in files:
        if filename.endswith('.json') and filename.startswith('test'):
            with open(os.path.join(dir, filename), 'rb') as f:
                case_data = json.load(f)
            cls_name = filename.replace('.json', '').replace('test', '').split('_')
            cls_name = 'Test' + ''.join([i.capitalize() for i in cls_name])
            cls = GenerateTest(cls_name, (HttpCase,), case_data)
            return unittest.defaultTestLoader.loadTestsFromTestCase(cls)


def parser_yaml_create_cases(dir: str):
    """解析yaml文件创建用例"""
    files = os.listdir(dir)
    for filename in files:
        # 支持json
        if filename.endswith('.yaml') and filename.startswith('test'):
            with open(os.path.join(dir, filename), 'rb') as f:
                case_data = yaml.load(f, Loader=yaml.FullLoader)
            cls_name = filename.replace('.yaml', '').replace('test', '').split('_')
            cls_name = 'Test' + ''.join([i.capitalize() for i in cls_name])
            cls = GenerateTest(cls_name, (HttpCase,), case_data)
            return unittest.defaultTestLoader.loadTestsFromTestCase(cls)
