# --coding:utf-8--


import os,platform

from loguru import logger

from common.path import ALLURE_FILES, ALLURE_REPORT
from config import test_info


class GV:
    """
    全局变量类
    """
    @classmethod
    def add_attr(cls, attr_name, attr_value):
        """
        添加类属性
        :param attr_name: 属性名
        :param attr_value: 属性值
        """
        setattr(cls, attr_name, attr_value)
        logger.info(f"已向 GVData 类添加属性 '{attr_name}'，其值为 '{attr_value}'。")

    @classmethod
    def delete_attr(cls, attr_name):
        """
        删除类属性
        :param attr_name: 属性名
        """
        if hasattr(cls, attr_name):
            delattr(cls, attr_name)
            logger.info(f"已从 GVData 类中删除属性 '{attr_name}'。")
        else:
            logger.warning(f"GVData 类中不存在属性 '{attr_name}'。")

    @classmethod
    def modify_attr(cls, attr_name, new_value):
        """
        修改类属性
        :param attr_name: 属性名
        :param new_value: 新的属性值
        """
        if hasattr(cls, attr_name):
            old_value = getattr(cls, attr_name)
            setattr(cls, attr_name, new_value)
            logger.info(f"已将 GVData 类中属性 '{attr_name}' 的值从 '{old_value}' 修改为 '{new_value}'。")
        else:
            logger.warning(f"GVData 类中不存在属性 '{attr_name}'，无法进行修改。")

    @classmethod
    def get_attr(cls, attr_name):
        """
        查询类属性
        :param attr_name: 属性名
        :return: 属性值，如果属性不存在返回 None
        """
        if hasattr(cls, attr_name):
            attr_value = getattr(cls, attr_name)
            return attr_value
        else:
            logger.warning(f"GVData 类中不存在属性 '{attr_name}'。")
            return None

    @classmethod
    def get_all(cls):
        """
        获取所有的全局变量，返回一个字典
        :return: 全局变量的字典
        """
        all_vars = {}
        for attr_name in dir(cls):
            # 排除特殊方法和属性，如 __dict__, __doc__, etc.
            if not attr_name.startswith("__"):
                all_vars[attr_name] = getattr(cls, attr_name)
        return all_vars

def gen_allure():
    try:
        # 记录运行环境
        with open(os.path.join(ALLURE_FILES, "environment.properties"), "w+") as f:
            f.write(f"OS {platform.system()}\n")
            f.write(f"Python Version:{platform.python_version()}\n")
            f.write(f"TestServer {test_info['host']}\n")
            f.write(f"DB {test_info['db']['database']}\n")
        # 生成测试报告
        os.system(f'allure generate {ALLURE_FILES} -o {ALLURE_REPORT} --clean')
        logger.info('测试报告已生成！')
        # os.system(f'allure open {ALLURE_REPORT}')
    except Exception as e:
        logger.info(f'测试报告生成失败:{e}')
        raise