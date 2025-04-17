# --coding:utf-8--

import os,datetime


#项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#case文件目录
CASE_DIR = os.path.join(BASE_DIR,'data')

# 日志目录
LOG_DIR = os.path.join(BASE_DIR,'logs')
#日志保留天数
LOG_SAVE_DAYS = 7
#日志文件名称
LOG_FILE_NAME = '{}_{}.log'.format('test',datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S'))
#日志文件保存路径
LOG_FULL_PATH = os.path.join(os.path.join(BASE_DIR,'logs'),LOG_FILE_NAME)



#allure_files
ALLURE_FILES = os.path.join(BASE_DIR,'reports','allure_files')

#测试报告
ALLURE_REPORT = os.path.join(BASE_DIR,'reports','report')


REPORT_JSON = os.path.join(BASE_DIR,'reports','report','widgets','summary.json')


if __name__ == '__main__':
    print(ALLURE_REPORT)