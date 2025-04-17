# --coding:utf-8--


import time,datetime
import json

import requests
from loguru import logger

from common.path import REPORT_JSON


def _calculate_pass_rate(json_file_path):
    try:
        # 打开并读取 JSON 文件
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # 从 JSON 数据中提取测试用例统计信息
        passed = data['statistic']['passed']
        total = data['statistic']['total']
        failed = data['statistic']['failed']
        skipped = data['statistic']['skipped']
        broken = data['statistic']['broken']

        # 计算执行时长
        duration = data['time']['stop'] - data['time']['start']
        duration = eval(f'{duration / 1000:.2f}')
        if duration < 60:
            duration = f'{duration:.2f}秒'
        else:
            minutes = int(duration // 60)
            duration = f'{int(minutes)}分{int(duration % 60)}秒'

        # 计算通过率
        if total == 0:
            pass_rate = 0
        elif (passed / total) * 100 == 100:
            pass_rate = '100%'
        else:
            pass_rate = f'{(passed / total) * 100:.2f}%'


        #记录运行时间
        # 获取当前时间戳
        timestamp = time.time()
        # 将时间戳转换为 datetime 对象并格式化
        date_str = datetime.datetime.fromtimestamp(timestamp).strftime("%m-%d %H:%M:%S")
        #测试报告查看地址
        report_link = f'http://192.168.1.67:8080/job/Runtest/allure/'


        result = {
            "report_link":report_link,
            "passed": passed,
            "total": total,
            "failed": failed,
            "skipped": skipped,
            "broken": broken,
            "duration": duration,
            "pass_rate": pass_rate,
            "date_str": date_str,
        }
        return result
    except FileNotFoundError:
        logger.info(f"未找到文件: {json_file_path}")
        return None
    except KeyError:
        logger.info("JSON 文件格式不符合预期，缺少必要的键。")
        return None
    except json.JSONDecodeError:
        logger.info("无法解析 JSON 文件。")
        return None



def send_feishu_message(webhook_url):
    """
    向飞书机器人发送消息
    :param webhook_url: 飞书机器人的 Webhook 地址
    :param pass_rate: 测试通过率
    """
    result = _calculate_pass_rate(REPORT_JSON)
    message = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "**执行结果**",
                    "content": [
                        [{"tag": "text", "text": f"**执行时间: {result['date_str']}"}],
                        [{"tag": "text", "text": f"🎯运行成功率: {result['pass_rate']}"}],
                        [{"tag": "text", "text": f"❤用例总数: {result['total']}"}],
                        [{"tag": "text", "text": f"😁成功用例数: {result['passed']}"}],
                        [{"tag": "text", "text": f"😭失败用例数: {result['failed']}"}],
                        [{"tag": "text", "text": f"😡阻塞用例数: {result['broken']}"}],
                        [{"tag": "text", "text": f"😶跳过用例数: {result['skipped']}"}],
                        [{"tag": "text", "text": f"🕓用例执行时长: {result['duration']}"}],
                        [{"tag": "a", "text": "点击查看测试报告>>", "href": f"{result['report_link']}"}],
                    ]
                }
            }
        }
    }
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        logger.info("飞书消息推送成功")
    except requests.exceptions.RequestException as e:
        logger.error(f"飞书消息发送失败: {e}")


if __name__ == '__main__':
    from config import test_info

    send_feishu_message(test_info['webhook'])