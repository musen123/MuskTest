"""
Author:柠檬班-木森
Time:2021/2/27 20:15
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
"""
import copy
import re
import json
import requests
import jsonpath
from apin.core.dataParser import DataParser
from apin.core.basecase import BaseTestCase
from apin.core import log
from apin.core.parsersetting import ENV


class CaseData:
    __attrs = ['url', 'method', 'params', 'data', 'json', 'files', 'headers', 'cookies', 'auth', 'timeout',
               'allow_redirects', 'proxies', 'hooks', 'stream', 'verify', 'cert']

    def __init__(self, title="", host="", interface="", extract=None, verification=None, url=None, method=None,
                 params=None, data=None, headers=None, cookies=None, files=None,
                 auth=None, timeout=None, allow_redirects=True, proxies=None,
                 hooks=None, stream=None, verify=None, cert=None, json=None, ):
        """Constructs a :class:`Request <Request>`, prepares it and sends it.
        Returns :class:`Response <Response>` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the
            :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
            :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the
            :class:`Request`.
        :param files: (optional) Dictionary of ``'filename': file-like-objects``
            for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable
            Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol or protocol and
            hostname to the URL of the proxy.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
        :rtype: requests.Response
        """
        self.title = title
        self.host = host
        self.interface = interface
        self.verification = verification
        self.extract = extract
        self.url = url
        self.method = method
        self.params = params
        self.data = data
        self.json = json
        self.files = files
        self.headers = headers
        self.cookies = cookies
        self.auth = auth
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.proxies = proxies
        self.hooks = hooks
        self.stream = stream
        self.verify = verify
        self.cert = cert
        self.datas = {}

    def data_handle(self, test):
        """请求数据处理"""
        # ------------如果用例没有设置url,method，headers则获取类属性中的------------------
        if not self.host:
            host = getattr(test, 'host', None) or ENV.get('host')
            if host:
                setattr(self, 'host', host)
            else:
                raise ValueError('用例参数host不能为空')
        if not self.interface:
            interface = getattr(test, 'interface', None) or ENV.get('interface')
            if interface:
                setattr(self, 'interface', interface)
            else:
                raise ValueError('用例参数interface不能为空')

        self.url = self.host + self.interface

        if not getattr(self, 'method', None):
            method = getattr(test, 'method', None) or ENV.get('method')
            if method:
                setattr(self, 'method', method)
            else:
                raise ValueError('用例参数method不能为空')

        if not getattr(self, 'headers', None):
            headers = getattr(test, 'headers', None) or ENV.get('headers')
            if headers:
                setattr(self, 'headers', headers)

        for k, v in self.__dict__.items():
            if k in self.__attrs:
                self.datas[k] = v

    def get(self, attr):
        return getattr(self, attr, None)


class Request:

    def __init__(self, case, test):
        """
        :param case: 用例数据
        :param test: 测试用例
        """
        self.test = test
        self.request_data = case

    def request_api(self):
        # 发送请求
        response = self.test.session.request(**self.request_data.datas)

        base_info = "[{}]: {} ".format(self.request_data.method.upper(), self.request_data.url)
        log.debug(base_info)
        self.test.url = self.request_data.url
        self.test.method = response.request.method
        self.test.status_cede = response.status_code
        self.test.base_info = base_info
        self.test.response_header = response.headers.items()
        self.test.requests_header = response.request.headers.items()
        try:
            response_body = response.json()
            self.test.response_body = json.dumps(response_body, ensure_ascii=False, indent=2)
        except:
            body = response.content
            self.test.response_body = body.decode('utf-8') if body else ''
        try:
            request_body = json.loads(response.request.body.decode('utf-8'))
            self.test.requests_body = json.dumps(request_body, ensure_ascii=False, indent=2)
        except:
            body = response.request.body
            self.test.requests_body = body.decode('utf-8') if body else ''
        self.requests_log(self.test)
        return response

    def requests_log(self, test):
        requests_log_info = "\n=======================Requests Info======================="
        requests_log_info += "\nRequest Headers:\n"
        for k, v in test.requests_header:
            requests_log_info += "      {}:{}\n".format(k, v)
        requests_log_info += "Request body:\n"
        requests_log_info += "{}".format(test.requests_body)
        response_log_info = "\n=======================Response Info======================="
        response_log_info += "\nResponse Headers:\n"
        for k, v in test.requests_header:
            response_log_info += "      {}:{}\n".format(k, v)
        response_log_info += "Response body:\n"
        response_log_info += test.response_body
        log.debug(requests_log_info)
        log.debug(response_log_info)


class Extract:
    """数据提取"""
    env = {}

    def json_extract(self, response, ext):
        """jsonpath数据提取"""
        value = jsonpath.jsonpath(response.json(), ext)
        value = value[0] if value else ''
        return value

    def re_extract(self, response, ext):
        """正则表达式提取数据提取"""
        value = re.search(ext, response.text)
        value = value.group(1) if value else ''
        return value


class HttpCase(BaseTestCase, Extract):
    host = None
    interface = None
    headers = None
    method = None
    Cases = []
    # 测试结果
    test_result = []
    session = requests.Session()

    def perform(self, case):
        log.info("开始执行用例：[{}]——>{}".format(case.get('title'), self))
        # 发送http请求
        response = self.http_requests(case)
        # 数据提取
        self.data_extraction(response, case)
        # 断言
        self.assert_result(response, case)

    def data_extraction(self, response, case):
        """
        数据提取
        :param response: response对象
        :param item: 要提数据的数据，列表嵌套字典
        :return:
        """
        exts = case.get('extract') or getattr(self, 'extract', None)

        if not isinstance(exts, dict): return
        # 遍历要提取的数据
        for name, ext in exts.items():
            # 判断提取数据的方式
            if len(ext) == 3 and ext[1] == "jsonpath":
                value = self.json_extract(response, ext[2])
            elif len(ext) == 3 and ext[1] == "re":
                value = self.re_extract(response, ext[2])
            else:
                log.warning("变量{},的提取表达式 :{}格式不对！".format(name, ext))
                break
            self.env[name] = value
            log.debug("提取变量：{},提取方式【jsonpath】,提取表达式:{},提取值为:{}".format(name, ext[2], value))

    def http_requests(self, case):
        # 发送请求
        # 处理请求数据
        case = self.handle_data(case)
        response = Request(case, self).request_api()
        return response

    def assert_result(self, response, case):
        """断言"""
        # 获取断言数据
        assert_list = case.get('verification') or getattr(self, 'verification', None)
        # 判断是否需要断言
        if assert_list and isinstance(assert_list, list):
            # 遍历断言的字段
            for item in assert_list:
                # 判断断言数据的类型
                if isinstance(item, list) and len(item) == 3:
                    self.__verification_list(response, item)
                elif len(item) == 3 and isinstance(item, dict):
                    self.__verification_dict(response, item)
                else:
                    raise ValueError('断言数据格式错误,verification字段为必须为数组，格式如下:\n'
                                     'verification:[\n'
                                     '[断言方式,预期结果,实际结果]\n'
                                     ']'
                                     '')
        elif assert_list:
            raise ValueError('断言数据格式错误,verification字段为必须为数组，格式如下:\n'
                             'verification:[\n'
                             '[断言方式,预期结果,实际结果]\n'
                             ']'
                             '')

    def __verification_list(self, response, item: list):
        # 判断断言的方法

        actual_pattern = r"V{{(.+?)}}"
        if item[0] == 'eq':
            if item[2] == "status_code":
                actual = response.status_code
                expected = item[1]
                log.info("预期结果：{} ".format(expected))
                log.info("实际结果：{}".format(actual))
                self.assertTrue(expected, actual)
                return
            act = item[2]
            actual = DataParser.parser_variable(self.env, act) if act else act
            if isinstance(actual, dict):
                for k, v in actual.items():
                    res = re.search(actual_pattern, v)
                    if res:
                        path = res.group(1)
                        v1 = self.json_extract(response, path)
                        v2 = self.re_extract(response, path)
                        value = v1 if v1 or v1 == 0 else v2
                        actual[k] = value
            elif isinstance(actual, list):
                for k, v in enumerate(copy.deepcopy(actual)):
                    res = re.search(actual_pattern, v)
                    if res:
                        path = res.group(1)
                        v1 = self.json_extract(response, path)
                        v2 = self.re_extract(response, path)
                        value = v1 if v1 or v1 == 0 else v2
                        actual[k] = value
            else:
                res = re.search(actual_pattern, actual)
                if res:
                    path = res.group(1)
                    v1 = self.json_extract(response, path)
                    v2 = self.re_extract(response, path)
                    value = v1 if v1 or v1 == 0 else v2
                    actual = value
            expected = item[1]
            expected = DataParser.parser_variable(self.env, expected) if expected else expected
            log.info("预期结果：{} ".format(expected))
            log.info("实际结果：{}".format(actual))
            # 断言
            self.assertEqual(expected, actual)
        elif isinstance(item, dict) and item.get('method') == 'contain':
            if item[2] == "status_code":
                actual = response.status_code
                expected = item[1]
                log.info("预期结果：{} ".format(expected))
                log.info("实际结果：{}".format(actual))
                self.assertTrue(expected, actual)
                return
            # 断言包含
            act = item.get('actual')
            actual = DataParser.parser_variable(self.env, act) if act else act
            for k, v in actual.items():
                res = re.search(actual_pattern, v)
                if res:
                    path = res.group(1)
                    v1 = self.json_extract(response, path)
                    v2 = self.re_extract(response, path)
                    value = v1 if v1 or v1 == 0 else v2
                    actual[k] = value
            expected = item.get('expected')
            expected = DataParser.parser_variable(self.env, expected) if expected else expected
            log.info("预期结果：{} ".format(expected))
            log.info("实际结果：{}".format(actual))
            self.assertIn(expected, actual)

    def __verification_dict(self, response, item):
        # 判断断言的方法
        actual_pattern = r"V{{(.+?)}}"
        if isinstance(item, dict) and item.get('method') == 'eq':
            act = item.get('actual')
            actual = DataParser.parser_variable(self.env, act) if act else act
            for k, v in actual.items():
                res = re.search(actual_pattern, v)
                if res:
                    path = res.group(1)
                    v1 = self.json_extract(response, path)
                    v2 = self.re_extract(response, path)
                    value = v1 if v1 or v1 == 0 else v2
                    actual[k] = value
            expected = item.get('expected')
            expected = DataParser.parser_variable(self.env, expected) if expected else expected
            log.info("预期结果：{} ".format(expected))
            log.info("实际结果：{}".format(actual))
            # 断言
            self.assertEqual(expected, actual)
        elif isinstance(item, dict) and item.get('method') == 'contain':
            # 断言包含
            act = item.get('actual')
            actual = DataParser.parser_variable(self.env, act) if act else act
            for k, v in actual.items():
                res = re.search(actual_pattern, v)
                if res:
                    path = res.group(1)
                    v1 = self.json_extract(response, path)
                    v2 = self.re_extract(response, path)
                    value = v1 if v1 or v1 == 0 else v2
                    actual[k] = value
            expected = item.get('expected')
            expected = DataParser.parser_variable(self.env, expected) if expected else expected
            log.info("预期结果：{} ".format(expected))
            log.info("实际结果：{}".format(actual))
            self.assertIn(expected, actual)

    def handle_data(self, case):
        """处理用例数据"""
        if isinstance(case, CaseData):
            data = case
        elif isinstance(case, dict):
            data = CaseData()
            for k, v in case.items():
                setattr(data, k, v)
        else:
            raise TypeError('请求数据只能为 dict 或 RequestData类型')

        for k, v in data.__dict__.items():
            if k not in ["extract", "verification"]:
                # 解析数据中的函数
                v = DataParser.parser_func(self.env, v)
                # 解析数据中的变量
                v = DataParser.parser_variable(self.env, v)
                setattr(data, k, v)
        data.data_handle(self)
        return data
