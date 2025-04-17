# --coding:utf-8--


import os

import pytest,allure

from common.gv import GV
#导入Utils基类，该类提供内置断言方式
from common.utils import Utils
from common.path import CASE_DIR
from common.base_api import api
from common.color_printer import ColorPrinter

#读取测试数据
datas = Utils.load_yaml(os.path.join(CASE_DIR,'test_api','user.yaml'))

#测试类继承Utils基类
class TestUser(Utils):

    @allure.title('{data[title]}')
    @pytest.mark.parametrize('data',datas['send_code'])
    def test_send_code(self,data):
        #这样可以清晰的看到执行的用例的名字
        ColorPrinter.print(f"执行用例: {data['title']}", color="magenta", bold=True)
        res = api.send_http(**data['account'])
        assert res.status_code == data['status']
        # Utils提供的数据提起及断言方法
        self.extract(res.json(), data['extract'])
        assert self.assert_eq(res.json(),data['expected'])


    @allure.title('{data[title]}')
    @pytest.mark.parametrize('data',datas['login'])
    def test_login(self,data):
        res = api.send_http(**data['account'])
        self.extract(res.json(),data['extract'])
        assert self.assert_eq(res.json(),data['expected'])

