# --coding:utf-8--


import os

import pytest, allure

from common.utils import Utils
from common.path import CASE_DIR
from common.base_api import BaseApi
from common.color_printer import ColorPrinter


datas = Utils.load_yaml(os.path.join(CASE_DIR,'test_scenario','address.yaml'))


@allure.feature("用户地址")
class TestAddress(Utils):

    @allure.title('{data[title]}')
    @pytest.mark.parametrize('data', datas['add_ress'])
    def test_address(self, data):
            #这样可以清晰的看到执行的用例的名字
        ColorPrinter.print(f"执行用例: {data['title']}", color="magenta", bold=True)
        res = BaseApi().send_http(**data['account'])
        assert self.assert_eq(res.json(), data['expected'])