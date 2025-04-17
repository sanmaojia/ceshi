# --coding:utf-8--


# 当前运行环境
env = 'test'

# test环境配置信息
if env == 'test':
    test_info = {
        # 测试主账号,用于登录获取token
        'account': {
            'mobile': 13012987185
        },
        'host': 'https://platform.raiserhealth.com/bk-api/',
        # 请求头
        'headers': {
            "charset": "utf-8",
            # "Content-Type": "application/x-www-form-urlencoded",
            "Content-Type": "application/json"},
        # 数据库配置
        'db': {
            "host": "localhost",
            "port": "port",
            "user": "user",
            "password": "password",
            "database": "database",
        },
        # 推送测试报告
        'webhook':'https://open.feishu.cn/open-apis/bot/v2/hook/b93e3311-5918-4cd0-ac19-3d1671b3d65d'

    }
elif env == 'production':
    pass
