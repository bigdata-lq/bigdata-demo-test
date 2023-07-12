## -*-coding:utf-8 -*-
#---------
# Name:lq  全量迁移
# Message: mysql数据迁入hdfs 隔天迁入
#---------

from etl.tools.escript import Escript

if __name__ == '__main__':
    #小视频审核关系表
    Escript(type = 'news_short_video').e_sqoop_whole_mysql2hive(hpath="/user/news/mysql/m_short_video_audit/", field= 'create_time', mname="short_video_audit")