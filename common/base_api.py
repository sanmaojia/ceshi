# --coding:utf-8--

import allure
import urllib3

import requests
from loguru import logger

from common.utils import Utils
from config import test_info
from common.gv import GV
from common.wrapper import api_log,singleton

@singleton
class BaseApi:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = test_info['headers']
        self.base_url = test_info['host']

    @api_log
    def send_http(self, method, url, data=None,  **kwargs):
        """
        :return: json
        """
        # 禁用 InsecureRequestWarning 警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            self._headers()
            url = self._url(url)
            allure.attach(str(self.session.headers), "请求头", allure.attachment_type.JSON)
            allure.attach(str(kwargs['json']), "请求参数", allure.attachment_type.JSON)
            if method.upper() == 'GET':
                response = self.session.get(url=url, params=data, verify=False, **kwargs)
            else:
                response = self.session.request(method=method, url=url, data=data,  verify=False, **kwargs)
            allure.attach(str(response.json()), "接口响应信息", allure.attachment_type.JSON)
            return response
        except requests.RequestException as e:
            # 处理请求异常，打印错误信息并重新抛出异常
            logger.error(f"请求发生错误: {e}")
            raise

    def _headers(self):
        """
        :param token: token处理
        :return:
        """
        # 如果GV中有Authorization属性，则将其添加到请求头中
        # 通过get_attr方法获取Authorization属性的值
        if hasattr(GV, 'Authorization'):
            self.session.headers.update({'Authorization': GV.get_attr('Authorization')})

    def _url(self, url):
        """
        :param url:URl处理 请求不同地址时写上完整路径
        :return:
        """
        if url.startswith("http://") or url.startswith("https://"):
            return url
        else:
            return self.base_url + url

    def login(self):
        #通过json表达式获取token，然后Utils.extract方法提取token
        # 提取token并存储到GV中
        response = requests.request(headers=test_info['headers'],method="POST",url=f"{test_info['host']}/user/login",json=test_info["account"])
        try:
            Utils.extract(response.json(),{"Authorization":"$..token"})
        except Exception as e:
            logger.warning(f'{e}')


api = BaseApi()

