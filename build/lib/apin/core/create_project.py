"""
Author:柠檬班-木森
Time:2020/7/28   17:12
E-mail:3247119728@qq.com
"""
# import os
# from shutil import copytree
# import apin
# from apin.core.logger import print_info
#
# template_path = os.path.join(os.path.dirname(os.path.abspath(apin.__file__)), 'templates')
# api_templates = os.path.join(template_path, 'http_demo')
#
#
# class ProjectManage(object):
#     @classmethod
#     def create_api(cls, name):
#         print_info("正在创建api自动化项目:{}".format(name))
#         try:
#             copytree(api_templates, os.path.join(".", name))
#         except Exception as e:
#             print_info("项目创建失败！:{}".format(e))
#         else:
#             print_info("项目创建成功！")
