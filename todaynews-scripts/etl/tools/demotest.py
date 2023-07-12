## -*-coding:utf-8 -*-
import sys
from etl.cons.data_param import *
from etl.tools.datasource import SourceDataframe
from etl.tools.escript import Escript
from etl.tools.send_mail import AldMail
from etl.cons.hive_param import HiveParam


if __name__ == '__main__':

    print(sys.path)
    # dicts={}
    # Param(dicts)
    # print(dicts)
    #
    # Escript().e_sqoop_hive2myql(hpath="/user/lq/remain/",mname="news_retain_report",fields="date_time,son_num,retain_num,retain_type")
    #
    # Escript().e_sqoop_increment_mysql2hive(htablename="lq.m_news_retain_report",hpath="/user/lq/remain1/", mname="news_retain_report")
    # #
    # Escript().e_sqoop_whole_mysql2hive(hpath="/user/lq/remain3/", mname="news_retain_report")
    #
    # df = SourceDataframe.read_hive(hql="select * from {}".format(HiveParam.LQ_M_NEWS_RETAIN_REPORT),
    #                                fields=["id","son_num","retain_num","retain_type","date_time","gmt_create","gmt_update","dt"])
    # print(df)
    #
    # df = SourceDataframe.read_myql(database="m_eps",sql="select * from news_app_analysis")
    #
    # html=AldMail.generate_html("测试邮件数据",df)
    # html1=AldMail.generate_html("测试邮件数据1",df)
    # html = AldMail.final_html(html,html1)
    # xlsx={
    #     "用户七日留存数据": df,
    #     "用户七日留存数据1": df
    # }
    # AldMail.send_mail("测试邮件数据", html, xlsx=xlsx,receivers=['liquan@astoutiao.com'])



