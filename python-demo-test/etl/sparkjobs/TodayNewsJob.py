#!/usr/bin/python
# -*- coding: utf-8 -*-
# author  :  lq
# 新闻召回集 job
# time    :  2018/9/6 15:30

from etl.tools.escript import Escript

sql = """
isRun=`yarn application -list -appStates RUNNING | grep TodayNewsJob | wc -l`
if [ \"$isRun\" =\"0\" ] ;then
    spark2-submit --master yarn --deploy-mode client --queue default --class com.alading.bigdata.news.lq.TodayNewsJob /lq/todaynews/alading-todaynews-news-jar-with-dependencies.jar
else
    echo \"已有同名的job在运行，状态码为：$results\"
fi
exit;
"""

if __name__ == "__main__":
    client = Escript(flag=True)
    client.excuse_hql(sql)