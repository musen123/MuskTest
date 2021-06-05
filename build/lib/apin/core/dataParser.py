"""
Author:柠檬班-木森
Time:2021/3/1 20:13
E-mail:3247119728@qq.com
"""
import importlib
import json
import re, sys, os
from numbers import Number
from apin.core import tools
from apin.core.parsersetting import ENV

sys.path.append(os.path.abspath('..'))
try:
    func_tools = importlib.import_module('funcTools')
except ModuleNotFoundError:
    from apin.templates.http_demo import funcTools as func_tools
# 函数的规则
func_pattern = r'F{(.*?)\((.*?)\)}'
# 变量的规则
variable_pattern = r'\${{.+?}}'
var2_pattern = r'\${{(.+?)}}'


class DataParser:
    """数据解析"""
    @classmethod
    def parser_func(cls, dic_attrs, data):
        """解析函数"""
        old_data = data
        if isinstance(data, str):
            while re.search(func_pattern, data):
                res2 = re.search(func_pattern, data)
                item = res2.group()
                # 获取函数名
                f_name = res2.group(1)
                # 提取函数的参数
                params = cls.get_func_params(res2, dic_attrs)
                # 执行函数
                func = getattr(func_tools, f_name, None) or getattr(tools, f_name, None)
                if not func:
                    raise ValueError('函数引用错误：\n{}\n中的函数{}未定义！,'.format(data, f_name))
                # 执行函数
                value = func(*params)
                if item == data: return value
                data = data.replace(item, str(value))
            return data
        elif isinstance(data, list) or isinstance(data, dict):
            data = str(data)
            while re.search(func_pattern, data):
                res2 = re.search(func_pattern, data)
                item = res2.group()
                # 获取函数名
                f_name = res2.group(1)
                # 提取函数的参数
                params = cls.get_func_params(res2, dic_attrs)
                func = getattr(func_tools, f_name, None) or getattr(tools, f_name, None)
                if not func:
                    raise ValueError('函数引用错误：\n{}\n中的函数{}没有定义！,'.format(
                        json.dumps(old_data, ensure_ascii=False, indent=2), f_name)
                    )
                # 执行函数
                value = func(*params)
                if isinstance(value, Number):
                    s = data.find(item)
                    dd = data[s - 1:s + len(item) + 1]
                    data = data.replace(dd, str(value))
                elif isinstance(value, str) and "'" in value:
                    data = data.replace(item, value.replace("'", '"'))
                else:
                    data = data.replace(item, value)
            return eval(data)
        else:
            return data

    @classmethod
    def get_func_params(cls, match_obj, dic_attrs):
        """解析函数的参数"""
        params = []
        # 提取函数的参数
        if match_obj.group(2):
            for i in match_obj.group(2).strip().split(','):
                # 判断参数中是否有变量
                if re.search(var2_pattern, i):
                    i = cls.parser_variable(dic_attrs, i)
                else:
                    # 判断是否双引号开头，是的话去除字符串
                    i = i[1:-1] if i.startswith('"') else eval(i)
                params.append(i)
        return params

    @classmethod
    def parser_variable(cls, dic_attrs, data):
        old_data = data
        """解析变量"""
        if isinstance(data, str):
            while re.search(var2_pattern, data):
                res2 = re.search(var2_pattern, data)
                item = res2.group()
                attr = res2.group(1)
                value = ENV.get(attr) if dic_attrs.get(attr) is None else dic_attrs.get(attr)
                if value is None:
                    raise ValueError('变量引用错误:\n{}中的变量{},在当前运行环境中未找到'.format(data, attr))

                if item == data: return value
                data = data.replace(item, str(value))
            return data
        elif isinstance(data, list) or isinstance(data, dict):
            data = str(data)
            while re.search(var2_pattern, data):
                res2 = re.search(var2_pattern, data)
                item = res2.group()
                attr = res2.group(1)
                value = ENV.get(attr) if dic_attrs.get(attr) is None else dic_attrs.get(attr)
                if value is None:
                    raise ValueError('变量引用错误：\n{}\n中的变量{},在当前运行环境中未找到'.format(
                        json.dumps(old_data, ensure_ascii=False, indent=2), attr)
                    )
                if isinstance(value, Number):
                    s = data.find(item)
                    dd = data[s - 1:s + len(item) + 1]
                    data = data.replace(dd, str(value))
                elif isinstance(value, str) and "'" in value:
                    data = data.replace(item, value.replace("'", '"'))
                else:
                    data = data.replace(item, value)
            return eval(data)
        else:
            return data
