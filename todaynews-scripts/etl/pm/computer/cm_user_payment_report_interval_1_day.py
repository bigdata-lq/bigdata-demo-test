## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 计算用户余额、金币报表
#---------

from etl.tools.escript import Escript
from etl.tools.datasource import SourceDataframe
from etl.cons.data_param import Param
from etl.tools.send_mail import AldMail

dicts= {}
Param(dicts)

## 计算用户余额、金币报表
hql = """
        set mapred.reduce.tasks=1;
        set hive.map.aggr=true;
        set hive.groupby.skewindata=true;
        set hive.exec.dynamic.partition.mode=nonstrict;
        set hive.merge.mapfiles=true;
        set  hive.merge.mapredfiles=true;
        set  hive.merge.size.per.task=64000000;
        insert into table aishangtoutiao.r_news_app_payment_report
        select
        date_add(current_date, -1) day_time,
        wind_type,
        round(sum(all_balance)/1000000,1) balance,
        round(sum(all_gold)/10000,1) gold,
        round(sum(if(c_user_id is null,no_frozen_balance,0))/1000000,1) no_frozen_balance,
        round(sum(if(c_user_id is null,no_frozen_gold,0))/10000,1) no_frozen_gold,
        count(DISTINCT a_user_id) all_num,
        sum(if(c_user_id is null,1,0))  no_frozen_num
        from
        (
        select
        CASE WHEN b.score >= 86 THEN '白名单'
             WHEN b.score >= 70 AND b.score < 86 THEN '灰名单'
             WHEN b.score >= 50 AND b.score < 70 THEN '一级黑名单'
             WHEN b.score < 50 THEN '二级黑名单'
        ELSE '无风控状态' END wind_type,
        (nvl(a.balance,0) + nvl(c.frozen_balance,0)) all_balance,
        (nvl(a.gold,0) + nvl(c.frozen_gold,0)) all_gold,
        nvl(a.balance,0) no_frozen_balance,
        nvl(a.gold,0) no_frozen_gold,
        a.user_id a_user_id,
        c.user_id c_user_id
        from aishangtoutiao.m_news_payment_wallet a
        left join
        aishangtoutiao.m_news_user_anti_score b
        on a.user_id = b.user_id
        left join
        (select user_id, sum(frozen_balance) frozen_balance, sum(frozen_gold) frozen_gold from aishangtoutiao.m_news_user_frozen_record where is_thaw = 0 group by user_id) c
        on a.user_id = c.user_id
        ) t group by wind_type ;
        """
## 读取mysql数据做报表展示
sql1 = """
        select
        day_time '日期',
        wind_type '风控状态',
        balance '总余额（单位/万）',
        gold '总金币（单位/万）',
        all_num '总用户数'
        from
        news_app_payment_report
        where day_time = '{day}'
        UNION ALL
        select
        day_time '日期',
        '总计' as '风控状态',
        round(sum(balance),1) '总余额（单位/万）',
        round(sum(gold),1) '总金币（单位/万）',
        round(sum(all_num),1) '总用户数'
        from
        news_app_payment_report
        where day_time = '{day}'
        """.format(day = dicts['ARG_TODAY_ISO_1'])

sql2 = """
        select
        day_time '日期',
        wind_type '风控状态',
        no_frozen_balance '无冻结用户总余额（单位/万）',
        no_frozen_gold '无冻结用户总金币（单位/万）',
        no_frozen_num '无冻结总用户数'
        from
        news_app_payment_report
        where day_time = '{day}'
        UNION ALL
        select
        day_time '日期',
        '总计' as '风控状态',
        round(sum(no_frozen_balance),1) '无冻结用户总余额（单位/万）',
        round(sum(no_frozen_gold),1) '无冻结用户总金币（单位/万）',
        round(sum(no_frozen_num),1) '无冻结总用户数'
        from
        news_app_payment_report
        where day_time = '{day}'
        """.format(day = dicts['ARG_TODAY_ISO_1'])


if __name__ == '__main__':

    # 计算用户余额、金币报表
    Escript().excuse_hql(hql,flag=True)

    # 迁移mysql
    Escript().e_sqoop_hive2myql(hpath="/user/news/pm/news_app_payment_report",
                                mname="news_app_payment_report",
                                fields="day_time,wind_type,balance,gold,no_frozen_balance,no_frozen_gold,all_num,no_frozen_num")
    # 发送邮件
    df1 = SourceDataframe.read_myql("m_eps",sql1)
    df2 = SourceDataframe.read_myql("m_eps",sql2)

    html1=AldMail.generate_html("全量用户余额、金币报表",df1)
    html2=AldMail.generate_html("无冻结用户用户余额、金币报表",df2)
    html = AldMail.final_html(html1,html2)
    # html = AldMail.final_html(html,html1)
    xlsx={
        "全量用户余额、金币报表": df1,
        "无冻结用户用户余额、金币报表": df1
    }
    AldMail.send_mail("全量用户余额、金币报表数据", html, xlsx=xlsx,
                      receivers=[
                                 'penghuaying@astoutiao.com',
                                 'hanyanchao@astoutiao.com',
                                 'zhengxiaoming@astoutiao.com',
                                 'fangyifan@astoutiao.com',
                                 'zhoujun@astoutiao.com'
                                 ])

