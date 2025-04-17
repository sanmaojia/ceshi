# --coding:utf-8--


import pytest
from loguru import logger

from common.path import LOG_FULL_PATH
from common.utils import Utils
from common.base_api import BaseApi
from common.gv import GV


@pytest.fixture(scope="session",autouse=True)
def fixture_session():
    logger.add(f'{LOG_FULL_PATH}', level='INFO', backtrace=True, diagnose=True, encoding='utf-8')
    logger.info("开始初始化")
    # 登录获取token
    
    BaseApi().login()




    yield 
    logger.info("开始后置清理程序")
    Utils.clean_logs()










