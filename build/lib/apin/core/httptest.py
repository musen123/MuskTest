# Author:柠檬班-木森
# E-mail:musen_nmb@qq.com
import copy
import re
import json
import requests
import jsonpath
from apin.core.dataParser import DataParser
from apin.core.initEvn import ENV, func_tools
from apin.core.basecase import BaseTestCase
from apin.core.logger import CaseLog


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


class Extract:
    """数据提取"""

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


class HttpCase(BaseTestCase, Extract, CaseLog):
    env = {}
    host = None
    interface = None
    headers = None
    method = None
    Cases = []
    # 测试结果
    test_result = []
    session = requests.Session()

    def perform(self, case):
        self.__run_log()
        # 发送http请求
        response = self.http_requests(case)

        # 数据提取
        self.data_extraction(response, case)
        self.__run_log()
        # 响应断言
        self.assert_result(response, case)

    def data_extraction(self, response, case):
        """
        数据提取
        :param response: response对象
        :param item: 要提数据的数据，列表嵌套字典
        :return:
        """
        exts = case.get('extract') or getattr(self, 'extract', None)
        if not (isinstance(exts, dict) and exts): return
        self.info_log("从响应结果中开始提取数据")
        self.extras = []
        # 遍历要提取的数据
        for name, ext in exts.items():
            # 判断提取数据的方式
            if len(ext) == 3 and ext[1] == "jsonpath":
                value = self.json_extract(response, ext[2])
            elif len(ext) == 3 and ext[1] == "re":
                value = self.re_extract(response, ext[2])
            else:
                self.error_log("变量{},的提取表达式 :{}格式不对！".format(name, ext))
                self.extras.append((name, ext, '提取失败！'))
                break
            if ext[0] == 'ENV':
                ENV[name] = value
            elif ext[0] == 'env':
                self.env[name] = value
            else:
                self.error_log("错误的变量级别，变量提取表达式中的变量级别只能为ENV，或者env".format(ext[1]))
                continue
            self.extras.append((name, ext, value))
            self.info_log("提取变量：{},提取方式【{}】,提取表达式:{},提取值为:{}".format(name, ext[1], ext[2], value))

    def http_requests(self, case):
        # 发送请求
        # 处理请求数据
        self.__request_hook(case, self.env, ENV)
        case = self.__handle_data(case)
        self.info_log('正在发送请求：')
        response = Request(case, self).request_api()
        self.__response_hook(case, response, self.env, ENV)
        self.response = response
        return response

    def assert_result(self, response, case):
        """断言"""
        self.assert_info = []
        # 获取断言数据
        assert_list = case.get('verification') or getattr(self, 'verification', None)
        # 判断是否需要断言
        if assert_list and isinstance(assert_list, list):
            # 遍历断言的字段
            for item in assert_list:
                # 判断断言数据的类型
                if isinstance(item, list) and len(item) == 3:
                    self.__verification(response, item)
                else:
                    raise ValueError("断言表达式 {} 格式错误:,\n断言表达式必须为如下格式：[断言方式,预期结果,实际结果]".format(item))
        elif assert_list:
            raise ValueError("""{}verification字段格式错误
            verification字段必须为如下格式：[
                [断言方式,预期结果,实际结果]
            ]""".format(assert_list))

    def __verification(self, response, item: list):
        self.info_log('断言表达式:{}'.format(item))
        # 判断断言的方法
        if item[2] == "status_code":
            if item[0] == 'eq':
                actual = response.status_code
                expected = item[1]
                self.info_log('断言http响应状态码是否和预期一致')
                return self.__assert(self.assertEqual, expected, actual, 'eq')
            else:
                self.error_log('http状态码，断言方式必须使用eq')
                raise ValueError('http状态码，断言方式必须使用eq')

        actual = self.__actualDataHandle(response, item[2])
        expected = item[1]
        expected = DataParser.parser_variable(self.env, expected) if expected else expected
        if item[0] == 'eq':
            self.info_log('断言响应数据中的实际结果是否和预期相等')
            self.__assert(self.assertEqual, expected, actual, 'eq')

        elif item[0] == 'contains':
            self.info_log('断言响应数据中的实际结果是否包含预期结果')
            self.__assert(self.assertIn, expected, actual, 'contains')
        else:
            raise ValueError('断言方法有误！断言方式只支持 eq 和 contains')

    def __handle_data(self, case):
        """处理用例数据"""
        if isinstance(case, CaseData):
            data = case
        elif isinstance(case, dict):
            data = CaseData()
            for k, v in case.items():
                setattr(data, k, v)
        else:
            raise TypeError('用例数据只能为dict类型CaseData类型')

        for k, v in data.__dict__.items():
            if k not in ["extract", "verification"]:
                # 解析数据中的函数
                v = DataParser.parser_func(self.env, v)
                # 解析数据中的变量
                v = DataParser.parser_variable(self.env, v)
                setattr(data, k, v)
        data.data_handle(self)
        return data

    def __run_log(self):
        """输出当前环境变量数据的日志"""
        self.l_env = ['{}:{}\n'.format(k, repr(v)) for k, v in self.env.items()]
        self.g_env = ['{}:{}\n'.format(k, repr(v)) for k, v in ENV.items()]
        self.debug_log("全局变量：\n{}".format(''.join(self.g_env)))
        self.debug_log("局部变量：\n{}".format(''.join(self.l_env)))

    def __actualDataHandle(self, response, act):
        """处理实际结果"""
        actual_pattern = r"V{{(.+?)}}"
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
        return actual

    def __assert(self, assert_method, expected, actual, method):
        """断言"""
        self.info_log("预期结果：{} ".format(expected))
        self.info_log("实际结果：{}".format(actual))
        try:
            assert_method(expected, actual)
        except AssertionError as e:
            self.assert_info.append((repr(expected), repr(actual), 'fail', method))
            self.warning_log('断言未通过')
            raise e
        else:
            self.assert_info.append((repr(expected), repr(actual), 'pass', method))
            self.info_log('断言通过！')

    def __request_hook(self, case, env, ENV):
        """请求钩子函数"""

        if case.get('request_hook'):
            self.info_log('执行请求钩子函数')
            try:
                exec(case.get('request_hook'))
            except Exception as e:
                self.error_log('请求钩子函数执行错误:\n{}'.format(e))

    def __response_hook(self, case, response, env, ENV):
        """响应钩子函数"""
        if case.get('response_hook'):
            self.info_log('执行响应钩子函数')
            try:
                exec(case.get('request_hook'))
            except Exception as e:
                self.error_log('响应钩子函数执行错误:\n{}'.format(e))

    @classmethod
    def __perform_fixture(cls, hook_name):
        if not hasattr(cls, hook_name):
            return
        hook = getattr(cls, hook_name)
        # 执行setup_hook方法
        if not isinstance(hook, str):
            raise ValueError('{}只能传递funcTools中定义的函数名,字符串类型'.format(hook_name))
        func = getattr(func_tools, hook)
        if not func:
            raise ValueError('函数引用错误：\n{}\n中的函数{}未定义！,'.format(func_tools, hook))
        return func

    def setUp(self):
        func = self.__perform_fixture('setup_hook', )
        if func:
            self.info_log('执行用例前置钩子函数')
            func(ENV, self.env)

    def tearDown(self):
        func = self.__perform_fixture('teardown_hook')
        if func:
            self.info_log('执行用例后置钩子函数')
            func(ENV, self.env, self.response)

    @classmethod
    def setUpClass(cls):
        func = cls.__perform_fixture('setup_class_hook')
        if func:
            cls.log.info('执行测试集前置钩子函数')
            func(ENV, cls.env)

    @classmethod
    def tearDownClass(cls):
        func = cls.__perform_fixture('teardown_class_hook')
        if func:
            cls.log.info('执行用测试集置钩子函数')
            func(ENV, cls.env)


class Request:

    def __init__(self, case, test: HttpCase):
        """
        :param case: 用例数据
        :param test: 测试用例
        """
        self.test = test
        self.request_data = case

    def request_api(self):

        # 发送请求
        try:
            self.test.url = self.request_data.datas.get('url')
            self.test.method = self.request_data.datas.get('method')
            response = self.test.session.request(**self.request_data.datas)
        except Exception as e:
            raise ValueError('请求发送失败，错误信息如下：{}'.format(e))
        base_info = "[{}]: {} ".format(self.request_data.method.upper(), self.request_data.url)
        self.test.debug_log(base_info)
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
            self.test.requests_body = body or ''
        self.requests_log(self.test)
        return response

    def requests_log(self, test):
        requests_log_info = "请求信息如下:"
        requests_log_info += "\nRequest Headers:\n"
        for k, v in getattr(test, 'requests_header'):
            requests_log_info += "      {}:{}\n".format(k, v)
        requests_log_info += "Request body:\n"
        requests_log_info += "{}".format(getattr(test, 'requests_body'))
        response_log_info = "接收后台的响应结果，响应信息如下:"
        response_log_info += "\nResponse Headers:\n"
        for k, v in getattr(test, 'requests_header'):
            response_log_info += "      {}:{}\n".format(k, v)
        response_log_info += "Response body:\n"
        response_log_info += getattr(test, 'response_body')
        self.test.debug_log(requests_log_info)
        self.test.debug_log(response_log_info)
