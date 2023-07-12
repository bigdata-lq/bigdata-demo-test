## -*-coding:utf-8 -*-
#---------
# Name:lq  全量迁移
# Message: mysql数据迁入hdfs 隔天迁入
#---------

from etl.tools.escript import Escript

if __name__ == '__main__':
    #用户金币冻结记录表
    Escript(type = 'news_payment').e_sqoop_whole_mysql2hive(hpath="/user/news/mysql/m_news_user_frozen_record/", mname="news_user_frozen_record")

    #用户金币冻结详情表
    Escript(type = 'news_payment').e_sqoop_whole_mysql2hive(hpath="/user/news/mysql/m_news_user_frozen_detail/", mname="news_user_frozen_detail ")