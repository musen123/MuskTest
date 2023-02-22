# 
## 1、概念介绍：

- **用例文件**：MuskTest中创建的每一个test开头的(py,json,yaml)文件，就是一个用例文件

- **用例集**：每个用例文件下可以创建多个用例集。一个用例集下面可以定义多条测试用例。
    - py用例文件中，一个测试类就是一个用例集
    - json用例文件最外层的数组中，一个对象就是一个用例集
    - yaml用例文件中,使用`testSet`来定义用例集

- **测试用例：** 用例集中Cases字段中的一条数据就是一个测试用例



## 2、用例集的主要字段介绍
**name：** 用例集的名字

```python
name = "登录场景用例"
```

**host：**用例接口的host地址(接口的域名) 

```python
host = "http://api.xxx.com/"
```

**headers：**指定用例使用的请求头

```python
headers = {"User-Agent": "musktest/musen"}
```

**method：**指定用例接口的请求方法

```python
method = 'post'
```

**interface：**指定用例接口地址（接口url域名后面的部分）

```python
interface = '/user/login'
```

**env：** 设置用例集运行环境的局部变量

```python
 env = {
        "user_mobile": '13109099878',
        "pwd": 'musk'
    }
```

**extract：**指定用例请求完要提取的变量（详细介绍见：**【四、变量提取和引用】**）

**verification：**指定用例的断言（详细介绍见：**【五、用例断言】**）

**Cases:**设置该测试集下的用例（详细介绍见：下一节【**用例字段介绍】**）

## 3、用例字段介绍

### 3.1、主要字段：

用例集中除env和Cases字段之外，上述用例集中的字段，均支持在用例中自定义。如果用例中定义了用例集中的字段，就使用自己定义的，没定义则引用 用例集中的。


​	**1、title：**用例的描述字段（必传字段）测试报告和日志信息中显示用例的描述

​	**2、json:** 用来传递json类型的请求参数，请求参数类型为：content-type:application/json，使用该字段来传递请求参数

​	**3、data：**用来传递表单类型的请求参数，请求参数类型为：content-type: application/x-www-form-urlencoded，使用该字段来传递请求参数

​	**4、params:** 用来查询字符串参数，请求参数，以？key=value的形式 拼接在url后面的参数

​	**5、files: **参数类型为：content-type:application/from-data，使用该字段来传递请求参数,常用于文件上传

```python
# 文件上传的参数格式支持如下两种传递形式
"files": {
	"fieldname": ["19.png", r"./image/19.png", "image/png"]
 }
#或
"files": [
    ("fieldname",["18.png", r"./image/18.png", "image/png"]),
    ("fieldname",["18.png", r"./image/18.png", "image/png"])
]

# 说明：
fieldname：为接口上传文件的参数名,后面列表中的参数值为,[文件类名，文件路径，文件类型]
    
```

​	


### 3.2、其他字段

除了上述主要字段之外，python中的requests库中的requests.request方法所有的请求参数，均支持在用例中定义字段，这些字段在大多数情况下都用不到，如果有用到


- **cookies：**请求的cookie信息（MuskTest中同一个用例集会自动化传递cookie,一遍情况下，不需要使用该字段来传递cookie）

- **auth:** 用于Basic/Digest/Custom HTTP认证

- **timeout：**设置http请求超时时间

- **allow_redirects：**是否运行请求重定向

- **proxies：**代理请求的

- **stream：**是否立即下载响应内容

- **verify：**是否进行证书校验（如果要忽略HTTPS请求的证书校验，则将此参数设置为False）

- **cert：**指定校验证书的路径

## 4、用例编写

### 4.1、python编写用例

**步骤一、**在case_py目录中定义一个以test开头的py文件，

**步骤二、**在文件中定义一个以Test开头的类，并且继承于MuskTest.core.httptest.HttpCase类

**步骤三、**在类中，编写测试集的字段值

```python
from musktest.core.httptest import HttpCase
class TestDomeV3(HttpCase):
    host = "http://api.xxxx.com/app/"
    headers = {"X-musk-Media-Type": "musk.v2"}
    # 定义测试前置方法
    setup_hook = 'get_timestamp'
    # 预设变量
    env = {
        "user_mobile": 'F{rand_phone("155")}',
        "admin_mobile": 'F{rand_phone("133")}'
    }
    # 结果校验
    verification = [
        ["eq", 0, 'V{{$..code}}'],
        ["eq", "OK", "V{{$..msg}}"]
    ]
```

**步骤四、**在Cases字段中编写用例数据

```python
from musktest.core.httptest import HttpCase
class TestDomeV3(HttpCase):
    host = "http://api.XXXX.com/app/"
    headers = {"X-musk-Media-Type": "musk.v2"}
    # 定义测试前置方法
    setup_hook = 'get_timestamp'
    # 预设变量
    env = {
        "user_mobile": 'F{rand_phone("155")}',
        "admin_mobile": 'F{rand_phone("133")}'
    }
    # 结果校验
    verification = [
        ["eq", 0, 'V{{$..code}}'],
        ["eq", "OK", "V{{$..msg}}"]
    ]
	Cases = [
        # 用例1：普通用户注册
        {
            'title': "普通用户注册",
            'interface': "member/register",
            "method": "post",
            'json': {"mobile_phone": "${{user_mobile}}", "pwd": "musk"},

        },
        # 用例2：管理员注册
        {
            'title': "管理员注册",
            'interface': "member/register",
            "method": "post",
            'json': {"mobile_phone": "${{admin_mobile}}", "pwd": "musk", "type":0}
        },
   ]
```



### 4.2、yaml编写用例

​	**注意点：使用yaml编写用例前 建议先去学习一下yaml的语法**

**步骤一：**在case_yaml目录中定义test开头的yaml文件

**步骤二：**在yaml文件中定义测试集，编写测试集中的用例

```yaml
# 定义一个用例集
- testSet:
    # 域名
    host: http://api.xxxxx.com/app/
    # 请求头
    headers:
      X-musk-Media-Type: musk.v2
    # 用例前置钩子函数
    setup_hook: get_timestamp
    # 预设运行变量
    env:
      user_mobile: F{rand_phone("155")}
      admin_mobile: F{rand_phone("133")}
    # 结果校验字段
    verification:
      - ["eq", 0, 'V{{$..code}}']
      - ["eq", "OK", "V{{$..msg}}"]
```

**步骤三：**在Cases字段中编写测试用例

```yaml
- testSet:
    # 域名
    host: http://api.xxxxx.com/app/
    # 请求头
    headers:
      X-musk-Media-Type: musk.v2
    # 用例前置钩子函数
    setup_hook: get_timestamp
    # 预设运行变量
    env:
      user_mobile: F{rand_phone("155")}
      admin_mobile: F{rand_phone("133")}
    # 结果校验字段
    verification:
      - ["eq", 0, 'V{{$..code}}']
      - ["eq", "OK", "V{{$..msg}}"]
    # 用例数据
    Cases:
      - title: 普通用户注册
        interface: member/register
        method: post
        json:
          mobile_phone: ${{user_mobile}}
          pwd: musk
      - title: 管理员注册
        interface: member/register
        method: post
        json:
          mobile_phone: ${{admin_mobile}}
          pwd: musk
          type: 0
```
如果一个用例文件中有多个用例集，则按照如下规范编写
```yaml
# 用例集1
- testSet:
    # 域名
    host: http://api.xxxxx.com/app/
    # 用例数据
    Cases:
      - title: 普通用户注册
        interface: member/register
        method: post
        json:
          mobile_phone: ${{user_mobile}}
          pwd: musk
# 用例集2
- testSet:
    # 域名
    host: http://api.xxxxx.com/app/
    # 用例数据
    Cases:
      - title: 普通用户注册
        interface: member/register
        method: post
        json:
          mobile_phone: ${{user_mobile}}
          pwd: musk
# 用例集3
- testSet:
    # 域名
    host: http://api.xxxxx.com/app/
    # 用例数据
    Cases:
      - title: 普通用户注册
        interface: member/register
        method: post
        json:
          mobile_phone: ${{user_mobile}}
          pwd: musk

```


### 4.3、json编写用例

使用yaml编写用例前 建议先去学习一下json的语法，json文件中字段名都需要使用双引号

**步骤一：**在case_json中定义一个test开头的json文件

**步骤二：**在json文件中定义一个数组，数组中定义一个对象就是一个测试集

**步骤三：**在测试集中定义相关的字段值和用例数据

```json
[
    {
      "host": "http://api.XXXXX.com/app/",
      "headers": {"X-musk-Media-Type": "musk.v2"},
      "setup_hook": "get_timestamp",
      "env": {
        "user_mobile": "F{rand_phone('155')}",
        "admin_mobile": "F{rand_phone('133')}"
      },
      "verification": [
        ["eq", {"code": 0, "msg": "OK"}, {"code": "V{{$..code}}", "msg": "V{{$..msg}}"}]
      ],
      "Cases": [
        {
          "title": "普通用户注册",
          "interface": "member/register",
          "method": "post",
          "json": {
            "mobile_phone": "${{user_mobile}}",
            "pwd": "musk"
          }
        },
        {
          "title": "管理员注册",
          "interface": "member/register",
          "method": "post",
          "json": {
            "mobile_phone": "${{admin_mobile}}",
            "pwd": "musk",
            "type": 0
          }
        }
      ]
    }
]
```