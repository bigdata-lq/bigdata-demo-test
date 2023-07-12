## -*-coding:utf-8 -*-
#---------
# Name:lq
# 执行时长：全量迁移
# Message: hive表数据全量迁移到msyql 隔天执行
#---------

from etl.tools.escript import Escript

if __name__ == '__main__':
    # 潮闻全栈pv汇总表
    Escript().e_sqoop_hive2myql(hpath="/user/news/mysql/news_app_pv/",
                                mname="news_app_pv_report",fields="day_time,view,cw_pv,sv_pv,ggj_pv,click")

    #编辑人员审核文章汇总表
    Escript().e_sqoop_hive2myql(hpath="/user/news/mysql/r_news_edit_day_count",
                                mname="news_edit_day_count_report",
                                fields="admin_name,check_time,jokenum,articlesum,shortnum,totalnum,jokesucced,articlesuccednum,shortsucceed,totalsuccednum,earlytime,lasttime")


    #编辑内容评论汇总数据
    Escript().e_sqoop_hive2myql(hpath="/user/news/mysql/r_news_comment_day_count",
                                mname="news_comment_day_count",
                                fields="author,check_time,jokenum,articlesum,shortnum,totalnum,jokesucced,articlesuccednum,shortsucceed,totalsuccednum,earlytime,lasttime")
