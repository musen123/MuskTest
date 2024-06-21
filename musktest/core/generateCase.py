# Author: -木森
# WeChart: python771
import unittest
import json
import os
import yaml
from musktest.core.httptest import HttpCase
from musktest.core.basecase import GenerateTest


class ParserDataToCase:
    @staticmethod
    def parser_json_create_cases(dir: str):
        """解析json文件创建用例"""
        suite = unittest.TestSuite()
        if os.path.isfile(dir) and dir.endswith('.json'):
            files = [os.path.split(dir)[1]]
            dir = os.path.split(dir)[0]
        elif os.path.isdir(dir):
            files = os.listdir(dir)
        else:
            return suite
        load = unittest.TestLoader()
        for filename in files:
            if filename.endswith('.json') and filename.startswith('test'):
                with open(os.path.join(dir, filename), 'rb') as f:
                    datas = json.load(f)
                cls_name = filename.replace('.json', '').replace('test', '').split('_')
                cls_name = 'Test' + ''.join([i.capitalize() for i in cls_name])
                index = 1
                for data in datas:
                    if isinstance(data, dict):
                        cls_name = cls_name + str(index)
                        index += 1
                        cls = GenerateTest(cls_name, (HttpCase,), data)
                        suite.addTest(load.loadTestsFromTestCase(cls))
        return suite

    @staticmethod
    def parser_yaml_create_cases(dir: str):
        """解析yaml文件创建用例"""

        suite = unittest.TestSuite()
        load = unittest.TestLoader()
        if os.path.isfile(dir) and dir.endswith('.yaml'):
            files = [os.path.split(dir)[1]]
            dir = os.path.split(dir)[0]
        elif os.path.isdir(dir):
            files = os.listdir(dir)
        else:
            return suite
        for filename in files:
            # 支持yaml
            if filename.endswith('.yaml') and filename.startswith('test'):
                with open(os.path.join(dir, filename), 'rb') as f:
                    datas = yaml.load(f, Loader=yaml.FullLoader)
                cls_name = filename.replace('.yaml', 'Yaml').replace('test', '').split('_')
                cls_name = 'Test' + ''.join([i.capitalize() for i in cls_name])
                index = 1
                for data in datas:
                    if isinstance(data, dict) and data.get('testSet'):
                        cls_name = cls_name + str(index)
                        index += 1
                        cls = GenerateTest(cls_name, (HttpCase,), data.get('testSet'))
                        suite.addTest(load.loadTestsFromTestCase(cls))
        return suite

    @staticmethod
    def parser_data_create_cases(datas):
        """
        解析数据创建用例
        :param data:
        :return:
        """
        suite = unittest.TestSuite()
        load = unittest.TestLoader()
        for index, data in enumerate(datas):
            cls_name = 'TestCase{}'.format(index)
            cls = GenerateTest(cls_name, (HttpCase,), data)
            suite.addTest(load.loadTestsFromTestCase(cls))
        return suite
