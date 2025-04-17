# --coding:utf-8--


import pymysql
from loguru import logger
from common.wrapper import singleton

@singleton
class MySql:
    """
    提供数据库方法
    """
    def __init__(self, **kwargs):
        try:
            self.con = pymysql.connect(charset="utf8",
                                       cursorclass=pymysql.cursors.DictCursor,
                                       **kwargs)
        except Exception as e:
            logger.error(f'数据库连接失败，连接参数：{kwargs}')
            raise e
        else:
            self.cur = self.con.cursor()

    def count(self, sql: str):
        """
        获取sql查询到的结果数量
        :param sql:
        :return:
        """
        count = self.cur.execute(sql)
        logger.info(f'执行sql: {sql}，获取结果条数为{count}')
        return count

    def update(self, sql: str):
        """
        执行更新sql，多条就往list内加字典
        :param sql: '[{"sql": "UPDATE boc_test SET audit = 1 WHERE id = xxxxx"}]'
        :return: self
        """
        sql_list = eval(sql)
        logger.info(f'要执行的update_sql为:{sql}')
        for sql in sql_list:
            try:
                self.cur.execute(sql['sql'])
                self.con.commit()
                logger.info("数据库更新成功！")
            except Exception:
                self.con.rollback()
                logger.exception("数据库更新失败！")
        return self

    def get_data(self,sql,size=1):
        """
        获取sql执行后数据
        :param sql:
        :param size: 指定游标获取结果条数
        :return:
        """
        count = self.count(sql)
        if count > 0:
            if count == 1:
                res = self.cur.fetchone()
            elif count == -1:
                res = self.cur.fetchall()
            elif count > 1:
                res = self.cur.fetchmany(size=size)
            else:
                res = False
                logger.warning(f'不支持获取size为:{size}的数据')
            logger.info(f'获取到的sql结果数据为：\n{res}')
            return res
        else:
            logger.info(f'执行{sql}以后的结果条数是:0')


    def close_connect(self):
        """
        关闭数据库连接
        :return:
        """
        # 关闭游标对象
        self.cur.close()
        # 断开连接
        self.con.close()
        logger.info('数据库连接已关闭！')