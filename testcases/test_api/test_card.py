# test_example.py
import os
import pytest
import allure

from common.gv import GV
from common.utils import Utils
from common.path import CASE_DIR
from common.base_api import api
from common.mysql import MySql
from common.color_printer import ColorPrinter

# 读取测试数据
datas = Utils.load_yaml(os.path.join(CASE_DIR, 'test_api', 'card.yaml'))

# 测试类
class TestUser(Utils):

    @allure.title('{data[title]}')
    @pytest.mark.parametrize('data', datas['header_card'])
    def test_send_code(self, data):
        # 打印当前执行的用例标题
        ColorPrinter.print(f"执行用例: {data['title']}", color="magenta", bold=True)

        # 发送请求（send_http 内部自动加 token）
        res = api.send_http(**data['account'])
        print("响应内容:", res.text)

        # 校验状态码
        assert res.status_code == data.get("status", 200), f"状态码校验失败！实际: {res.status_code}"

        # 提取变量到变量池
        self.extract(res.json(), data.get("extract", {}))

        # 动态替换 expected 变量（如 $channelNo）
        data = self.prepare_expected(data)

        # 断言返回结果与期望是否一致
        assert self.assert_eq(res.json(), data['expected']), f"断言失败！预期: {data['expected']}"
