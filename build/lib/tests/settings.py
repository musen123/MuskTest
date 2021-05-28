"""
测试项目的配置

"""
import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))
# 日志文件路径
LOG_FILE_PATH = os.path.join(BASEDIR, "./logs")



# 是否为debug模式
DEBUG = True

# 数据库配置
DB = {

}

# 测试环境配置
ENV = {
    "host":"http://api.lemonban.com/futureloan/",

}



# 测试结果配置
TEST_RESULT = {
    # 测试报告名称
    "filename": "report.html",
    # 测试人员
    "tester": "测试员",
    # 报告标题
    "title": "测试报告",
    # 报告样式
    "templates": 1,
    # 报告描述信息
    "desc": "XX项目测试生成的报告"
}

# # 邮箱通知配置
EMAIL = {
    # smtp服务器地址
    "host": '',
    # smtp服务器端口
    "port": "",
    # 邮箱账号
    "user": "",
    # smtps授权码
    "password": "",
    # 收件人列表
    "to_addrs": [],
    # 是否发送附件
    "is_file": True
}
#
# # 钉钉通知
# DINGTALK = {
#     #  钉钉机器人的Webhook地址
#     "url": "",
#     # 如果钉钉机器人安全设置了关键字，则需要传入对应的关键字
#     "key": None,
#     # 如果钉钉机器人安全设置了签名，则需要传入对应的密钥
#     "secret": None,
#     # 钉钉群中要@人的手机号列表，如：[137xxx,188xxx]
#     "atMobiles": [],
#     # 是否@所有人
#     "isatall": False
# }
#
# # 企业微信通知
# WECHAT = {
#     # chatid:企业微信群ID
#     "chatid": "",
#     # access_token:调用企业微信API接口的凭证
#     "access_token": ""
# }
