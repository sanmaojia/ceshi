# --coding:utf-8--


import pytest

from common.gv import gen_allure
from config import test_info
from send_msg import send_feishu_message

if __name__ == '__main__':
    #按照pytest.ini配置的规则收集并执行用例
    pytest.main()
    #全部执行完毕后生成测试报告
    gen_allure()
    # 发送飞书消息通知
    send_feishu_message(test_info['webhook'])