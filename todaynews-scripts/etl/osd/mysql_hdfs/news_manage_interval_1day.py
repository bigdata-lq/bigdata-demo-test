## -*-coding:utf-8 -*-
#---------
# Name:lq  全量迁移
# Message: mysql数据迁入hdfs 隔天迁入
#---------

from etl.tools.escript import Escript

if __name__ == '__main__':
    #咕咕鸡审核表1
    Escript(type = 'news_manage').e_sqoop_whole_mysql2hive(hpath="/user/news/mysql/m_news_joke_check_log/", mname="news_joke_check_log")

    #潮闻审核表
    Escript(type = 'news_manage').e_sqoop_whole_mysql2hive(hpath="/user/news/mysql/m_news_article_check_log/", mname="news_article_check_log ")

    #审核关系表
    Escript(type = 'news_manage').e_sqoop_whole_mysql2hive(hpath="/user/news/mysql/m_news_admin_user/", mname="news_admin_user ")