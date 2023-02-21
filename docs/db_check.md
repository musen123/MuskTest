# 


### 数据库校验

## 1、基本配置说明

如果要在用例中进行数据库校验，首先需要在settting.py中添加数据库的相关配置，配置如下

**单个数据库配置**

```python
DB = [
	# 数据库连接名
    {"name": "aliyun",
     # 数据库类型（目前仅支持mysql）
     "type": "mysql",
     # 数据库的基本配置
     "config": {
         'user': "root",
         "password": "123456",
         "host": "127.0.0.1",
         "port": 3306}
     }
]
```

**多个数据库配置**

如果项目测试中，需要连接多个数据库服务，进行数据查询操作，apin支持添加多个数据库配置来实现对多个数据库连接并操作。具体配置如下

```python
DB = [
    # 数据库1
    {"name": "aliyun",
     "type": "mysql",
     "config": {
         'user': "root",
         "password": "123456",
         "host": "api.xxx.com",
         "port": 3306}
     },
    # 数据库2
    {"name": "qcd",
     "type": "mysql",
     "config": {
         'user': "root",
         "password": "123456",
         "host": "www.lemon.com",
         "port": 3306}
     }
]
```



## 2、钩子函数参数说明：

apin中提供了一个`db_check_hook`字段用来之指定用数据库验的钩子函数，数据库校验的钩子函数和前后置钩子函数一样，都是定义在 funcTools 文件中。

数据库校验的钩子函数在定义时，需要定义如下几个参数。

| 参数名 | 说明                                 |
| ------ | ------------------------------------ |
| test   | 当前执行的测试用例,                  |
| db     | 操作数据库的对象（详细使用见下一节） |
| ENV    | 全局环境变量                         |
| env    | 局部环境变量                         |

**钩子函数定义示例：**

```python
def register_db_check(test, db, ENV, env):
    sql = "SELECT count(*) as count FROM user"
    # 前置sql查询
    s_count = db.qcd.execute(sql)['count']
    yield
    # 后置sql查询
    e_count = db.qcd.execute(sql)['count']
    # 返回sql校验表达式
    return [
        ['eq', 1, e_count-s_count]
    ]
```

## 3、db对象的使用

接下来我们来看看关于钩子函数中接收到的db这个数据库操作对象如何使用。为了实现同时对多个数据库操作的支持，我们需要通过db选择数据库，再对数据库进行操作。

**3.1、数据库的选取：`qcd = db.数据库名  `**

​		数据库名就是配置中name字段的值

**案例：**

setting.py中的数据库配置如下，数据库配置的name字段为aliyun，那么选择这个数据库就使用`db.aliyun`

```python
DB = [{"name": "aliyun",
     "type": "mysql",
     "config": {
         'user': "root",
         "password": "123456",
         "host": "127.0.0.1",
         "port": 3306}}]
```

**3.2、sql执行的方法**

通过db对象选中具体的数据库对象之后，就可以调用execute方法来执行sql语句

```python
sql = "SELECT count(*) as count FROM user"
# 调用execute执行sql
s_count = db.qcd.execute(sql)
```

**3.3、执行结果数据获取**

execute执行之后返回的是一个字典，查询出来的字段名作为key,字段值作为value,通过字典键取值的方式就可以获取到查询的结果了

```python
sql = "SELECT count(*) as count FROM user"
# 调用execute执行sql
res = db.qcd.execute(sql)
# 获取查询出来的count字段
count = res['count']
```



## 5、用例执行前后的sql查询

在很多测试场景下，我们会需要在用例执行前后，分别对数据库进行查询，在apin的钩子函数中，只需要通过`yield`来隔开用例执行前后的数据库操作即可，`yield`之前的操作会在用例执行之前执行，yield之后的操作会在用例执行之后执行。

```python
# 前置sql查询
s_res = db.qcd.execute(sql)
yield
# 后置sql查询
e_res = db.qcd.execute(sql)
```

## 6、校验表达式

关于数据校验，直接在钩子函数中通过retrun把要校验的表达式返回出来即可,校验表达式格式如下

```python
# 校验表达式
[
     ['校验方式', '预期结果1', '实际结果1'],
     ['校验方式', '预期结果2', '实际结果2'],
     ....
 ]
```



## 7、钩子函数的使用

在编写用例时可以通过`db_check_hook`指定用例数据库校验的钩子函数，下面以yaml文件为例

```yaml
-testSet:
    # 域名
    host: http://api.lemonban.com/futureloan/
    # 指定用例前置钩子函数
    setup_hook: random_phone_hook
    # 用例数据
    Cases:
      - title: 普通用户注册
        interface: member/register
        # 指定数据库校验的钩子函数
        db_check_hook: register_db_check
        method: post
        json:
          mobile_phone: ${{user_mobile}}
          pwd: lemonban
```




