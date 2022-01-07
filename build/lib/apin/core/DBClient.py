"""
============================
Project: Apin
Author:柠檬班-木森
Time:2021/7/6 17:23
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
Site: http://www.lemonban.com
Forum: http://testingpai.com 
============================
"""


class DBMysql:
    """mysql databases"""

    def __init__(self, config):
        import pymysql
        config['autocommit'] = True
        self.con = pymysql.connect(**config)
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)

    def execute(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchone()

    def execute_all(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def __del__(self):
        self.cur.close()
        self.con.close()


class DBClient:

    def __init__(self, DB):
        for config in DB:
            if not config.get('name'): raise ValueError('数据库配置的name字段不能为空！')
            if config.get('db'):
                setattr(self, config.get('name'), config.get('db'))
            elif config.get('type').lower() == 'mysql' and config.get('config'):
                setattr(self, config.get('name'), DBMysql(config.get('config')))
            else:
                raise ValueError('您传入的数据库配置有误，或者apin目前不支持：{}'.format(config))
