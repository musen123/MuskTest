# Author:木森
# WeChart: python771
import argparse
import os
import time
import unittest
from shutil import copytree
import musktest
from musktest.core.initEvn import settings, log, ENV
from musktest.core.testRunner import TestRunner
from musktest.core.logger import print_info
from musktest.core.generateCase import ParserDataToCase


def create(args):
    """创建项目"""
    if hasattr(args, "name"):
        name = args.name
        template_path = os.path.join(os.path.dirname(os.path.abspath(musktest.__file__)), 'templates')
        api_templates = os.path.join(template_path, 'http_demo')
        print_info("正在创建接口自动化项目:{}".format(name))
        try:
            copytree(api_templates, os.path.join(".", name))
        except Exception as e:
            print_info("项目创建失败！:{}".format(e))
        else:
            print_info("项目创建成功！")


def run(args=None):
    """run test"""
    log.info('开始执行测试，加载用例....')
    if isinstance(args, argparse.Namespace):
        args = args
    else:
        if args is None:
            args = create_parser().parse_args(['run'])
        elif args[0] != 'run':
            args = create_parser().parse_args(['run'] + args)
        else:
            args = create_parser().parse_args(args)
    if hasattr(args, "file"):
        dir = os.path.abspath(getattr(args, 'file'))
    else:
        # help info
        dir = os.path.abspath('.')
    if os.path.isfile(dir):
        if dir.endswith('.yaml'):
            suite = ParserDataToCase.parser_yaml_create_cases(dir)
        elif dir.endswith('.json'):
            suite = ParserDataToCase.parser_json_create_cases(dir)
        elif dir.endswith('.py'):
            suite = unittest.defaultTestLoader.discover(os.path.dirname(dir), pattern=os.path.split(dir)[1])
        else:
            suite = unittest.TestSuite()
    elif os.path.isdir(dir):
        # load TestCase
        # load yaml TestCase
        yaml_dir = os.path.join(dir, 'case_yaml')
        suite1 = ParserDataToCase.parser_yaml_create_cases(yaml_dir)
        # load json TestCase
        json_dir = os.path.join(dir, 'case_json')
        suite2 = ParserDataToCase.parser_json_create_cases(json_dir)
        # load py TestCase
        case_dir = os.path.join(dir, 'case_py')
        suite3 = unittest.defaultTestLoader.discover(case_dir)
        suite = unittest.TestSuite()
        suite.addTest(suite1)
        suite.addTest(suite2)
        suite.addTest(suite3)
    else:
        suite = unittest.TestSuite()
    if suite == unittest.TestSuite():
        log.error('未加载到用例,请确认指定的用例路径或者目录是否正确！')
        log.error('执行路径为：{}'.format(dir))
        return
    # Test Result
    result = getattr(settings, 'TEST_RESULT', {})
    report_name = result.get('filename') if result.get('filename') else "report.html"
    result['filename'] = report_name

    runner = TestRunner(suite=suite, **result)
    res = runner.run(thread_count=getattr(args, "thread") or getattr(settings, 'THREAD', 1),
                     rerun=getattr(args, "rerun") or getattr(settings, 'RERUN', 0),
                     interval=getattr(args, "interval") or getattr(settings, 'INTERVAL', 2)
                     )

    if hasattr(settings, 'EMAIL'):
        try:
            # 邮件通知处理配置
            for k, v in getattr(settings, 'EMAIL').items():
                if not v:
                    raise ValueError("邮件参数配置有误,setting.py文件中的EMAIL的 {} 字段不能为空".format(k))
            else:
                runner.send_email(**getattr(settings, 'EMAIL'))
        except Exception  as e:
            log.error("测试结果邮件推送失败：{}".format(e))
        else:
            log.info("测试结果已发送到邮箱")
    if hasattr(settings, 'DINGTALK'):
        try:
            res = runner.dingtalk_notice(**settings.DINGTALK)
        except Exception as e:
            log.error("发送钉钉通知出错了，错误信息如下:{}".format(e))

        else:
            if res["errcode"] == 0:
                log.info("测试结果推送到钉钉群成功！")
            else:
                log.error("测试结果推送到钉钉群失败！错误信息:  {}".format(res["errmsg"]))
    if hasattr(settings, 'WECHAT'):
        try:
            res = runner.weixin_notice(**settings.WECHAT)
        except Exception as e:
            log.error("测试结果推送到企业微信出错了，错误信息如下:  {}".format(e))
        else:
            if res["errcode"] == 0:
                log.info("测试结果推送到企业微信成功！")
            else:
                log.error("测试结果推送到企业微信失败！错误信息： {}".format(res["errmsg"]))

    return res


def create_parser():
    parser = argparse.ArgumentParser(prog='musktest', description='ApiTest使用命令介绍')
    # 添加版本号
    parser.add_argument('-V', '--version', action='version', version='%(prog)s 1.1.3')
    subparsers = parser.add_subparsers(title='Command', metavar="命令")
    # 创建项目命令
    create_cmd = subparsers.add_parser('create', help='create test project ', aliases=['C'])
    create_cmd.add_argument('name', metavar='project_name', help="project name")
    create_cmd.set_defaults(func=create)
    # 运行项目命令
    parser_run = subparsers.add_parser('run', help='run test project', aliases=['R'])
    parser_run.add_argument('--file', type=str, metavar='file', help='case file path', default='.')
    parser_run.add_argument('--thread', type=int, metavar='thread', help='Concurrent running thread', default=None)
    parser_run.add_argument('--rerun', type=int, metavar='rerun', help='Number of failed case reruns', default=None)
    parser_run.add_argument('--interval', type=int, metavar='interval', help='Rerun interval', default=None)
    parser_run.set_defaults(func=run)
    return parser


def main(params: list = None):
    """
    程序入口
    :param params: list
    :return:
    """
    parser = create_parser()
    # 获取参数
    if params:
        args = parser.parse_args(params)
    else:
        args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()



if __name__ == '__main__':
    main(['create', '../demo2'])
