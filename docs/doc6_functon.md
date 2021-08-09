# 

apin支持在测试用例中调用自定义的函数来处理数据，如对数据进行加密处理、随机生成数据等等。

### 1、自定义函数

apin创建的项目中有一个funcTools.py，在该文件中可以自己定义函数，然后在用例中通过F{xxx()}来调用。

- **案例：funcTools.py文件**

```python
import hashlib,random

def md5_encrypt(msg):
    """md5加密"""
    md5 = hashlib.md5()  
    md5.update(msg.encode("utf8"))  
    return md5.hexdigest()

def rand_phone():
	"""随机生成手机号的函数"""
    import random
    for i in range(8):
        phone += str(random.randint(0, 9))
    return str(phone)


def get_timestamp():
    """获取时间戳"""
    return time.time()

```

- **注意点：函数处理完的数据需要return返回哦**

### 2、用例中引用函数

- **引用表达式：F{函数名()}**

    用例数据中的user，引用前面定义的rand_phone函数

```python
{
	'title': "普通用户注册",
	'interface': "member/register",
	"method": "post",
	'json': {"user": "F{rand_phone()}", "pwd": "lemon123"},
}
```

用例数据中的pwd，引用前面定义的md5_encrypt函数对密码进行md加密

- **注意点：引用的函数，传递的参数如果是变量，则不需要在变量应用表达式外加引号**

```python
{
	'title': "普通用户登录",
	'interface': "member/login",
	"method": "post",
	'json': {"user": "13109877890", "pwd": "F{md5_encrypt('lemon123')}"},
}

# 引用函数，变量作为参数传递
{
	'title': "普通用户登录",
	'interface': "member/login",
	"method": "post",
	'json': {"user": "${{user}}", "pwd": "F{md5_encrypt(${{pwd}})}"},
}
```

### 3、apin内置工具函数

在`apin.core.tools`模块中内置了一些常用的工具函数中，创建项目生成的funcTools.py,默认导入了apin中内置的所有工具函数，这些工具函数可以直接在自定义工具函数或编写用例时使用，接下来给大家介绍一下apin中内置的工具函数。

apin中的工具函数分为两类，一类是生成测试数据的，一类是用来处理数据的。

##### 数据处理的函数

**1、base64_encode：base64编码**

```
入参: 字符串
返回值: base64编码之后的内容
```

**2、md5_encrypt: MD5加密**

```
入参: 明文内容(字符串)
返回值:MD5加密之后的密文
```

**3、rsa_encrypt:RSA非对称加密**

```
入参1:明文内容(字符串)
入参2: RSA公钥
返回值:加密之后的密文
```



##### 数据生成的函数

**1、random_mobile：随机生成手机号码**

**2、random_name：随机生成中文名**

**3、random_city：随机生产城市名**

**4、random_email：随机生成邮箱账号**

**5、random_ipv4：随机生产一个ipV4的地址**

**6、random_date：随机生产一个日期**

**7、radom_date_time:随机生成一个时间**

**8、random_postcode：随机生产一个邮编**

**9、random_company：随机生成一个公司名**

**10、random_addr：随机生成一个地址**

**11、random_ssn：随机生产一个省份证号**

**12、get_timestamp：获取当前时间戳**