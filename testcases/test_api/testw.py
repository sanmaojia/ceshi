#调试专用文件
import sys
import os

# 将项目根路径添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import requests
from common.gv import GV
from common.mysql import MySql
"""
def test():
    token = GV.get_attr('Authorization')
    headers = {'Authorization': token}
    url = 'https://platform.raiserhealth.com/bk-api/patient/bindList'
    data = {"productUserId":"1215"}
    res = requests.post(url=url, headers=headers, json=data,)
    print("这是测试的内容",res.text)
"""


def test():
    url = 'https://platform.raiserhealth.com/bk-api/user/login'
    headers = {'Content-Type': 'application/json'}
    data = {
        "mobile": '13012987185'
    }
    res = requests.post(url=url, headers=headers, json=data)
    print("这是测试的内容", res.text)
    #print("这是测试的内容", res.json()['data']['token'])
    token= res.json()['data']['token']
    user_id = res.json()['data']['user']['id']
    print(f"登录成功，token: {token}")
    print(f"返回的用户ID: {user_id}")

    # 数据库连接
    db = MySql(
        host='rm-bp1x0611cpj02f6r7.mysql.rds.aliyuncs.com',
        user='root',
        password='Ruize@2024',
        database='rz_health_equity',
        port=3306
    )

    # 通过 user_id 查询用户信息
    sql = f"SELECT * FROM product_user_active WHERE user_id = {user_id}"  # 注意替换成你的真实表名
    result = db.get_data(sql)

    if result:
        print(f"数据库中查询到的用户信息: {result}")
    else:
        print("数据库中未查询到该用户！")

    db.close_connect()
    id = result['product_user_id']



    headers = {'Authorization': f'Bearer {token}'} 
    url = "https://platform.raiserhealth.com/bk-api/equity/productUserDetail"
    data = {"productUserId":id,'notLoading':True}
    res = requests.post(url=url, headers=headers, json=data,)
    print("这是测试的内容",res.status_code)



test()


