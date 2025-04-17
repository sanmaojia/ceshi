# -*- coding: utf-8 -*-


from functools import wraps

from jsonpath import jsonpath
from loguru import logger


def api_log(func):
    """
    接口请求记录
    :param func:
    :return: response
    """
    @wraps(func)
    def inner(*args,**kwargs):
        try:
            url = kwargs.get('url')
            method = kwargs.get('method')
            json_data = kwargs.get('json')
            form_data = kwargs.get('data')
            # 记录请求信息
            if url:
                logger.info(f'请求接口：{url}')
            else:
                logger.warning('请求参数中未提供 url！')
            if method:
                logger.info(f'请求方式：{method}')
            else:
                logger.warning('请求参数中未提供 method！')
            if json_data:
                logger.info(f'请求 JSON 参数：{json_data}')
            if form_data:
                logger.info(f'请求表单参数：{form_data}')
        except Exception as e:
            logger.error(f'记录请求信息时出现异常：{e}')
        try:
            # 调用原函数并获取响应
            res = func(*args, **kwargs)
            # 记录响应信息
            try:
                json_body = res.json()
                logger.info(f'响应 body（JSON 格式）：\n{json_body}')
            except ValueError:
                logger.warning('响应 body 不是有效的 JSON 类型！')
                text_body = res.text
                logger.info(f'响应 body（文本格式）：\n{text_body}')
            logger.info(f'响应状态码：{res.status_code}')
        except Exception as e:
            logger.error(f'调用接口或记录响应信息时出现异常：{e}')
            res = None
        return res
    return inner


def assert_log(func):
    """
    断言日志记录
    :param func:
    :return: response
    """
    @wraps(func)
    def inner(*args,**kwargs):
        if args[2] is None or args[2] == 'None':
            logger.warning('传入的预期结果为 None')
        elif args[2]:
            logger.info(f'jsonpath表达式：{[key for key, value in args[2].items()]}')
            logger.info(f'预期结果: {[value for key, value in args[2].items()]}')
            logger.info(f'实际结果: {[jsonpath(args[1], key)[0] for key, value in args[2].items()]}')
        else:
            logger.warning('传入的预期结果参数为 None')
        res = func(*args, **kwargs)
        try:
            if res == True:
                logger.info('断言结果: 成功')
        except AssertionError as e:
            logger.error('断言结果: 失败!')
            raise e

        return res
    return inner


def singleton(cls):
    # 单例模式 创建一个字典来存储类和对象的映射关系
    dic = {}
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if dic.get(cls):
            return dic[cls]
        else:
            dic[cls] = cls(*args, **kwargs)
            return dic[cls]
    return wrapper



