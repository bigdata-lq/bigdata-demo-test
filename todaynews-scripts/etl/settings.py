# -*- coding: utf-8 -*-

# mysql测试环境配置
mysql_dev_eps_settings = {
    "host": "192.168.115.105:3306",
    "user": "root",
    "password": "Hik12345+",
    "charset": "utf8",
    "database": "m_eps"
}

mysql_dev_payment_settings = {
    "host": "192.168.115.105:3306",
    "user": "root",
    "password": "Hik12345+",
    "charset": "utf8",
    "database": "news_payment"
}

mysql_dev_manage_settings = {
    "host": "192.168.115.105:3306",
    "user": "root",
    "password": "Hik12345+",
    "charset": "utf8",
    "database": "news_manage"
}

mysql_dev_short_video_settings = {
    "host": "192.168.115.105:3306",
    "user": "root",
    "password": "Hik12345+",
    "charset": "utf8",
    "database": "news_short_video"
}


hive_dev_settings = dict(
    hostname='192.168.115.170',
    port=22,
    username='root',
    password='hik12345'
)

spark_dev_settiings = dict(
    hostname='192.168.115.167',
    port=22,
    username='root',
    password='hik12345'
)


# 邮箱配置
mail_settings = {
    "mail_host": "smtp.exmail.qq.com",  # 设置服务器
    "mail_user": "dashuju@astoutiao.com",  # 用户名
    "mail_pass": "Dsj123.",  # 口令
    "sender": "dashuju@astoutiao.com",  # 邮件发送人
    # 邮件接收人列表 批量发送
    "receivers": [
        'liquan@astoutiao.com',
        'huangyali@astoutiao.com'
    ]
}

# mysql_settings = {
#     "news_payment" : mysql_dev_payment_settings,
#     "m_eps": mysql_dev_eps_settings,
#     "news_manage": mysql_dev_manage_settings,
#     "news_short_video": mysql_dev_short_video_settings
# }
#
# hive_settings = hive_dev_settings
# spark_settings = spark_dev_settiings

#### 线上环境 ####
mysql_online_payment_settings = {
    "host": "10.81.3.63:17066", # payment mysql 数据库
    "user": "dsjread",
    "password": "dsjread@123",
    "charset": "utf8",
    "database": "news_payment"
}

mysql_online_eps_settings = {
    "host": "10.81.3.40:17066", # eps mysql 数据库
    "user": "eps_user",
    "password": "eps_user@2019",
    "charset": "utf8",
    "database": "m_eps"
}

mysql_online_manage_settings = {
    "host": "10.81.3.15:3306",
    "user": "root",
    "password": "Hik12345+",
    "charset": "utf8",
    "database": "news_manage"
}

mysql_online_short_video_settings = {
    "host": "10.81.3.15:3306",
    "user": "root",
    "password": "Hik12345+",
    "charset": "utf8",
    "database": "news_short_video"
}

hive_online_settings = dict(
    hostname='10.81.1.214',
    port=10036,
    username='root',
    password='Alading@2017'
)

spark_online_settiings = dict(
    hostname='10.81.1.216',
    port=10036,
    username='root',
    password='Alading@2017'
)

meta_settings = {
    "host": "rm-bp10q4q9cwc1f267p717.mysql.rds.aliyuncs.com:3306",
    "user": "group_data",
    "password": "GJvSbAn84Y9mIFRx",
    "charset": "utf8",
    "database": "meta"
}

mysql_settings = {
    "news_payment" : mysql_online_payment_settings,
    "m_eps": mysql_online_eps_settings,
    "news_manage": mysql_online_manage_settings,
    "news_short_video": mysql_online_short_video_settings,
    "meta": meta_settings
}
hive_settings = hive_online_settings
spark_settings = spark_online_settiings
