# --coding:utf-8--
import json
from string import Template
import datetime,os

import yaml
from faker import Faker
from loguru import logger
from jsonpath import jsonpath


from common.gv import GV
from common.wrapper import assert_log
from common.path import LOG_DIR, LOG_SAVE_DAYS

from string import Template
import yaml


class Utils:
    """提供工具方法"""

    @classmethod
    def load_yaml(cls, file_path: str):
        """
        读取指定路径的 YAML 文件，并返回解析后的数据
        :param file_path:
        :return:
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                yaml_data = yaml.safe_load(file)
            return yaml_data
        except FileNotFoundError:
            logger.error(f'YAML 文件未找到，文件路径：{file_path}')
            raise
        except yaml.YAMLError as yaml_error:
            logger.error(f'YAML 文件解析失败，文件路径：{file_path}，错误信息：{str(yaml_error)}')
            raise
        except Exception as general_error:
            logger.error(f'读取 YAML 文件时发生未知错误，文件路径：{file_path}，错误信息：{str(general_error)}')
            raise


    @classmethod
    def template(cls, source_data:dict, replace_data: dict):
        """
        替换文本变量
        :param source_data: 数据源   {phone: $phone}
        :param replace_data:要替换的数据 {phone: 'new_phone'}
        :return:
        """
        res = Template(str(source_data)).safe_substitute(**replace_data)
        return yaml.safe_load(res)

    def prepare_expected(self, data):
        '''可以直接帮助我动态替换预期结果中的变量'''
         # 1. 获取变量池中的所有数据
        extracted = GV.get_all() 
         # 2. 替换 expected 中的变量
        data["expected"] = self.template(data["expected"], extracted) 
        # 3. 返回更新后的 data
        return data  




    @classmethod
    def template1(cls, source_data: dict, replace_data: dict):
        """
        支持在 Python 端循环替换 list 类型的变量：
        - 如果 replace_data 中所有的 list 值长度相同，则按索引并行循环
        - 否则按单次替换返回单个对象

        :param source_data:  原始数据结构，值中可包含 $placeholder
        :param replace_data: 要替换的内容，支持 list（批量）或单值
        :return: 单个对象或对象列表
        """
        # 找出所有 list 类型的替换项
        list_keys = [k for k, v in replace_data.items() if isinstance(v, list)]
        if list_keys:
            # 校验所有 list 长度一致
            lengths = [len(replace_data[k]) for k in list_keys]
            if not all(l == lengths[0] for l in lengths):
                raise ValueError("所有 list 类型的替换项必须等长")
            results = []
            # 并行循环，每次取出同一索引的替换值
            for idx in range(lengths[0]):
                single_data = {
                    k: (v[idx] if isinstance(v, list) else v)
                    for k, v in replace_data.items()
                }
                # 安全替换
                rendered = Template(str(source_data)).safe_substitute(**single_data)  # :contentReference[oaicite:1]{index=1}
                results.append(yaml.safe_load(rendered))
            return results
        else:
            # 单次替换
            rendered = Template(str(source_data)).safe_substitute(**replace_data)
            return yaml.safe_load(rendered)



    @classmethod
    def clean_logs(cls):
        now = datetime.datetime.now()
        for root, dirs, files in os.walk(LOG_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                # 获取文件的修改时间
                mtime = os.path.getmtime(file_path)
                modified_date = datetime.datetime.fromtimestamp(mtime)
                # 计算文件的存在天数
                delta = now - modified_date
                if delta.days > LOG_SAVE_DAYS:
                    os.remove(file_path)
                    logger.info(f"已清理{LOG_SAVE_DAYS}天前没修改过的日志文件！")


    @classmethod
    def handle_random_phone(cls):
        """
        生成随机手机号
        :return:
        """
        fake = Faker(locale='zh_CN')
        phone_number = fake.phone_number()
        return phone_number


    @classmethod
    def extract(cls,resp:dict,expr=None):
        """
        提取响应结果
        :param resp: json
        :param expr: {"token":"$..token"}
        :return:
        """
        if expr == None or expr =='None':
            logger.warning('提取表达式为空！')
        else:
            for key, value in expr.items():
                actual = jsonpath(resp, value)[0]
                if key == 'Authorization':
                    actual = 'Bearer '+ actual
                if actual is not None:
                    GV.add_attr(key,actual)
                else:
                    logger.warning('没有提取到数据')


    @classmethod
    @assert_log
    def assert_eq(cls,resp: dict, expr: dict):
        """
        equals 等于
        :param resp: json
        :param assert_expr: 提取表达式:预期结果  {"$..status":1,"$..msg":"登录成功"}
        :return: True或者False
        """
        if expr == None or expr =='None':
            return True
        elif resp and expr:
            for key, value in expr.items():
                actual = jsonpath(resp, key)[0]
                try:
                    assert actual == value
                except:
                    return False
            return True
        elif not expr:
            return True
        else:
            return False

    @classmethod
    @assert_log
    def assert_neq(cls, resp: dict, expr: dict):
        """
        not equals 不等于
        :param resp: json
        :param assert_expr: 提取表达式:预期结果  {"$..status":1,"$..msg":"登录成功"}
        :return: True或者False
        """
        if expr == None or expr == 'None':
            return True
        elif resp and expr:
            for key, value in expr.items():
                actual = jsonpath(resp, key)[0]
                try:
                    assert actual != value
                except:
                    return False
            return True
        else:
            return False

    @classmethod
    @assert_log
    def assert_gt(cls, resp: dict, expr: dict):
        """
        greater than 大于
        :param resp: json
        :param assert_expr: dict
        :return: True或者False
        """
        if expr == None or expr == 'None':
            return True
        elif resp and expr:
            for key, value in expr.items():
                actual = jsonpath(resp, key)[0]
                try:
                    assert actual > value
                except:
                    return False
            return True
        else:
            return False

    @classmethod
    @assert_log
    def assert_lt(cls, resp: dict, expr: dict):
        """
        less than 小于
        :param resp: json
        :param assert_expr: dict
        :return: True或者False
        """
        if expr == None or expr == 'None':
            return True
        elif resp and expr:
            for key, value in expr.items():
                actual = jsonpath(resp, key)[0]
                try:
                    assert actual < value
                except:
                    return False
            return True
        else:
            return False

    @classmethod
    @assert_log
    def assert_ge(cls, resp: dict, expr: dict):
        """
        greater than or equals 大于等于
        :param resp: json
        :param assert_expr: dict
        :return: True或者False
        """
        if expr == None or expr == 'None':
            return True
        elif resp and expr:
            for key, value in expr.items():
                actual = jsonpath(resp, key)[0]
                try:
                    assert actual >= value
                except:
                    return False
            return True
        else:
            return False

    @classmethod
    @assert_log
    def assert_le(cls, resp: dict, expr: dict):
        """
        less than or equals 小于等于
        :param resp: json
        :param assert_expr: dict
        :return: True或者False
        """
        if expr == None or expr == 'None':
            return True
        elif resp and expr:
            for key, value in expr.items():
                actual = jsonpath(resp, key)[0]
                try:
                    assert actual <= value
                except:
                    return False
            return True
        else:
            return False


if __name__ == '__main__':
    print(json.dumps(Utils.load_yaml('/Users/a1234/PycharmProjects/RzApiTest/data/test_api/user.yaml')))
