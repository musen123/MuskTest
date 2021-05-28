"""
Author:柠檬班-木森
Time:2020/8/26   11:25
E-mail:3247119728@qq.com
"""
import json
import re
import traceback
import unittest
import time
from apin.core.parsersetting import ENV
from apin.core import log


class TestResult(unittest.TestResult):
    """ 测试结果记录"""

    def __init__(self):
        super().__init__()

        self.fields = {
            "success": 0,
            "all": 0,
            "fail": 0,
            "skip": 0,
            "error": 0,
            "begin_time": "",
            "results": [],
            "testClass": set()
        }

    def startTest(self, test):
        """
        当测试用例测试即将运行时调用
        :return:
        """
        super().startTest(test)
        self.start_time = time.time()

    def stopTest(self, test):
        """
        当测试用列执行完成后进行调用
        :return:
        """
        # 获取用例的执行时间
        test.run_time = '{:.3}s'.format((time.time() - self.start_time))
        test.class_name = test.__class__.__qualname__
        test.method_name = test.__dict__['_testMethodName']
        test.method_doc = test.shortDescription()
        self.fields['results'].append(test)
        self.fields["testClass"].add(test.class_name)

    def stopTestRun(self, title=None):
        """
        测试用例执行完手动调用统计测试结果的相关数据
        :param title:
        :return:
        """
        self.fields['fail'] = len(self.failures)
        self.fields['error'] = len(self.errors)
        self.fields['skip'] = len(self.skipped)
        self.fields['all'] = sum(
            [self.fields['fail'], self.fields['error'], self.fields['skip'], self.fields['success']])
        self.fields['testClass'] = list(self.fields['testClass'])

    def addSuccess(self, test):
        """用例执行通过，成功数量+1"""
        self.fields["success"] += 1
        test.state = '成功'
        log.info("{}执行——>【通过】\n".format(test))
        log.debug("当前运行环境全局变量有：\n{}\n".format(json.dumps(ENV, ensure_ascii=False, indent=2)))
        log.debug("当前运行环境局部变量有：\n{}\n".format(json.dumps(getattr(test, 'env'), ensure_ascii=False, indent=2)))

        test.run_info = getattr(test, 'base_info', None)


    def addFailure(self, test, err):
        """
        :param test: 测试用例
        :param err:  错误信息
        :return:
        """
        super().addFailure(test, err)
        test.state = '失败'
        log.debug("当前运行环境全局变量有：\n{}\n".format(json.dumps(ENV, ensure_ascii=False, indent=2)))
        log.debug("当前运行环境局部变量有：\n{}\n".format(json.dumps(getattr(test, 'env'), ensure_ascii=False, indent=2)))
        log.warning("{}执行——>【失败】\n".format(test))
        # 保存错误信息
        log.warning(err[1])
        log.exception(err)
        test.run_info = getattr(test, 'base_info', None)


    def addSkip(self, test, reason):
        """
        修改跳过用例的状态
        :param test:测试用例
        :param reason: 相关信息
        :return: None
        """
        super().addSkip(test, reason)
        test.state = '跳过'
        log.info("{}执行--【跳过Skip】\n".format(test))
        test.run_info = reason

    def addError(self, test, err):
        """
        修改错误用例的状态
        :param test: 测试用例
        :param err:错误信息
        :return:
        """
        super().addError(test, err)
        test.state = '错误'
        log.error('\n' + "".join(traceback.format_exception(*err)))
        log.debug("当前运行环境全局变量有：\n{}\n".format(json.dumps(ENV, ensure_ascii=False, indent=2)))
        log.debug("当前运行环境局部变量有：\n{}\n".format(json.dumps(getattr(test, 'env'), ensure_ascii=False, indent=2)))
        log.error("{}执行——>【错误Error】\n".format(test))
        log.exception(err)
        if test.__class__.__qualname__ == '_ErrorHolder':
            test.run_time = 0
            res = re.search(r'(.*)\(.*\.(.*)\)', test.description)
            test.class_name = res.group(2)
            test.method_name = res.group(1)
            test.method_doc = test.shortDescription()
            self.fields['results'].append(test)
            self.fields["testClass"].add(test.class_name)
        test.run_info = getattr(test, 'base_info',None)


class ReRunResult(TestResult):

    def __init__(self, count, interval):
        super().__init__()
        self.count = count
        self.interval = interval
        self.run_cases = []

    def startTest(self, test):
        if not hasattr(test, "count"):
            super().startTest(test)

    def stopTest(self, test):
        if test not in self.run_cases:
            self.run_cases.append(test)
            super().stopTest(test)

    def addFailure(self, test, err):
        """
        :param test: 测试用例
        :param err:  错误信息
        :return:
        """
        if not hasattr(test, 'count'):
            test.count = 0
        if test.count < self.count:
            test.count += 1
            log.error("{}执行——>【失败Failure】\n".format(test))
            log.exception(err)
            log.error("================{}重运行第{}次================\n".format(test, test.count))
            time.sleep(self.interval)
            test.run(self)
        else:
            super().addFailure(test, err)
            if test.count != 0:
                log.debug("================重运行{}次完毕================\n".format(test.count))

    def addError(self, test, err):
        """
        修改错误用例的状态
        :param test: 测试用例
        :param err:错误信息
        :return:
        """
        if not hasattr(test, 'count'):
            test.count = 0
        if test.count < self.count:
            test.count += 1
            log.error("{}执行——>【错误Error】\n".format(test))
            log.exception(err)
            log.error("================{}重运行第{}次================\n".format(test, test.count))
            time.sleep(self.interval)
            test.run(self)
        else:
            super().addError(test, err)
            if test.count != 0:
                log.debug("================重运行{}次完毕================\n".format(test.count))
