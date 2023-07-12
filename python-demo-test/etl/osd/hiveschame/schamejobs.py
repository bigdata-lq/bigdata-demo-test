## -*-coding:utf-8 -*-
#---------
# Name:lq  全量迁移
# Message: mysql数据迁入hdfs 隔天迁入
#---------

from etl.tools.hiveutil import HiveUtil
from etl.tools.datasource import SourceDataframe


if __name__ == '__main__':
    # 金币冻结记录表
    HiveUtil.changeMysql2Hive("news_payment","news_user_frozen_record","/user/news/mysql/m_news_user_frozen_record")

    # 咕咕鸡审核表
    HiveUtil.changeMysql2Hive("news_manage","news_joke_check_log","/user/news/mysql/m_news_joke_check_log")
    #潮闻审核表
    HiveUtil.changeMysql2Hive("news_manage","news_article_check_log","/user/news/mysql/m_news_article_check_log")
    #审核关系表
    HiveUtil.changeMysql2Hive("news_manage","news_admin_user","/user/news/mysql/m_news_admin_user")
    # 小视频审核表
    HiveUtil.changeMysql2Hive("news_short_video","short_video_audit","/user/news/mysql/m_short_video_audit")
