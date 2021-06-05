import base64
import random
import time
import rsa


def rand_phone(phone='155'):
    """随机生成手机号"""
    for i in range(8):
        phone += str(random.randint(0, 9))
    return str(phone)


def get_timestamp():
    """生成当前时间戳"""
    return time.time()


def ras_encrypt(msg, server_pub):
    """
    rsa加密
    :param msg: 待加密文本
    :param server_pub: 密钥
    :return:
    """
    msg = msg.encode('utf-8')
    pub_key = server_pub.encode("utf-8")
    public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)  #
    cryto_msg = rsa.encrypt(msg, public_key_obj)  # 生成加密文本
    cipher_base64 = base64.b64encode(cryto_msg)  # 将加密文本转化为 base64 编码
    return cipher_base64.decode()
