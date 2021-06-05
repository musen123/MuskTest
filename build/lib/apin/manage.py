import argparse
import os, sys
import time
import unittest
from apin import TestRunner, Load
from apin.core.create_project import ProjectManage
from apin.core.parsersetting import ParserDB, settings
from apin.core import log

sys.path.append(os.getcwd())


class GlobalData:
    if getattr(settings, 'DB', None):
        db = ParserDB()
    # debug模式
    DEBUG = getattr(settings, 'DEBUG', None)
    # 运行线程
    thread_count = getattr(settings, 'THREAD_COUNT', 1)


def create(args):
    """创建项目"""
    if hasattr(args, "name"):
        # 创建项目
        ProjectManage.create_api(args.name)


def run(args=None):
    """run test"""
    args = args if isinstance(args, argparse.Namespace) else create_parser().parse_args(args)

    if hasattr(args, "test_dir"):
        dir = os.path.abspath(args.test_dir)
    else:
        # help infp
        dir = os.path.abspath('.')
    from apin.core import parserCase
    # load TestCase
    # load yaml TestCase
    data_dir = os.path.join(dir, 'casedata')
    suite1 = parserCase.parser_yaml_create_cases(data_dir) or unittest.TestSuite()
    # load json TestCase
    suite2 = parserCase.parser_json_create_cases(data_dir) or unittest.TestSuite()
    # load py TestCase
    case_dir = os.path.join(dir, 'testcases')
    suite = unittest.defaultTestLoader.discover(case_dir)
    suite.addTest(suite1)
    suite.addTest(suite2)
    # Test Result
    result = getattr(settings, 'TEST_RESULT', {})
    report_name = result.get('filename') if result.get('filename') else "report.html"
    result['filename'] = time.strftime('%Y-%m-%d_%H_%M_%S') + report_name

    runner = TestRunner(suite=suite,
                        report_dir=os.path.join(dir, 'reports'),
                        **result)
    runner.run(thread_count=GlobalData.thread_count)
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


def create_parser():
    parser = argparse.ArgumentParser(prog='apin', description='ApiTest使用命令介绍')
    # 添加版本号
    parser.add_argument('-V', '--version', action='version', version='%(prog)s 0.0.5')
    subparsers = parser.add_subparsers(title='Command', metavar="命令")
    # 创建项目命令
    create_cmd = subparsers.add_parser('create', help='create test project ', aliases=['C'])
    create_cmd.add_argument('name', metavar='project_name', help="project name")
    create_cmd.set_defaults(func=create)
    # 运行项目命令
    parser_run = subparsers.add_parser('run', help='run test project', aliases=['R'])
    parser_run.add_argument('-test_dir', metavar='test_dir', help='case file path', default='.')
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
