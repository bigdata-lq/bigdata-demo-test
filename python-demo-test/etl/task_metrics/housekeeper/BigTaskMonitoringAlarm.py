## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 监控0~7点任务执行时长超过40min任务
#---------
import sys
import pymysql
import pandas as pd
import datetime
import os

start_time = datetime.datetime.now().strftime('%Y-%m-%d')
end_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

## 白名单
taskNameList = [
    'st_selfhelp_order_new_d',
    'lfm_als_submit_external',
    'kylin_tele_sales_order_cube_v2',
    'operate_data_center_base_cube',
    'kylin_tele_sales_shop_cube',
    'split_ods_pt_trade_supply_d_run',
    'dw_operate_data_center_v2_d',
    'dw_index_shop_count_d',
    'kylin_operate_data_center_search_keyword',
    'model_usercf_submit_external',
    'dw_order_trade_supply_d',
    'split_ods_pt_order_pay_d_run',
    'split_ods_pt_settlement_clearing_detail_d_run',
    'ads_hpc_shp_shop_flow_behavior_tag_d',
    'split_ods_wxd_seller_price_d_run',
    'split_ods_pt_trade_shop_d_run',
    'operate_data_center_search_order_v2',
    'split_ods_pt_wxd_on_sale_item_d_run',
    'ads_order_biz_order_channel_d',
    'split_ods_pt_settlement_liquidation_d_run',
    'st_discrete_shop_features_test_d',
    'split_ods_pt_settlement_clearing_d_run',
    'st_reco_front_category_first_item_d',
    'dw_gross_profit_all_d_test',
    'report_shop_transform_ratio_d',
    'st_discrete_shop_features_d',
    'ads_prm_channel_storey_d',
    'sync_fin_dw_gross_profit_all_d',
    'split_ods_pt_order_logistics_d_run'
]


task_40_min_sql = """
select 
name, start_time, end_time, process_time, waiting_time
from 
(
select 
j.name, h.start_time, h.gmt_create, h.end_time,
TIMESTAMPDIFF(second,h.start_time,h.end_time) process_time,
TIMESTAMPDIFF(second,h.gmt_create,h.start_time) waiting_time
from hera_job j
left join 
hera_action_history h
on j.id = h.job_id
where j.auto = 1 
and    h.gmt_create > '{start_time}' and h.gmt_create < '{end_time}'
and    j.name not like 'dqc%' 
and    h.is_nrt = 0 -- 0离线，1准实时
and    h.trigger_type = 1 -- 1自动调度,2手动触发,3手动恢复
and    substr(h.start_time,12,8) >= '00:00:00'
and    substr(h.end_time,12,8) <=   '07:00:00'         -- 根据当前时间来设置 
and    h.status='success'
) temp where process_time > 2400 order by process_time DESC
""".format(start_time = start_time, end_time = end_time)

print(task_40_min_sql)

## hirac jdbc参数信息
hirac_settings = {
    "host": "pc-bp18pmc60uu8bm043.rwlb.rds.aliyuncs.com:3306",
    "user": "streaming_pdb",
    "password": "xOMZ0AbeeIlKDqyi",
    "charset": "utf8",
    "database": "hirac"
}

mysql_settings = {
    "hirac": hirac_settings
}


class MysqlUtil(object):

    @staticmethod
    def read_myql(database,sql):
        """
        MYSQL语句返回dataframe
        """
        databaseInfo = {}
        database = mysql_settings[database]
        params = database["host"].split(":")
        databaseInfo['host'] = params[0]
        databaseInfo['port'] = int(params[1])
        databaseInfo['user'] = database['user']
        databaseInfo['password'] = database['password']
        databaseInfo['database'] = database['database']
        databaseInfo['charset'] = database['charset']
        databaseInfo['connect_timeout'] = 200
        mysql_client = pymysql.connect(**databaseInfo)
        df = pd.read_sql(sql, mysql_client)
        df.fillna("", inplace=True)
        mysql_client.close()
        return df

if __name__ == '__main__':
    df = MysqlUtil.read_myql("hirac", task_40_min_sql)

    ding_text = "hirac离线新增耗时超过40min信息通知\\n任务名,　　　　　　　　开始时间,　　　　结束时间,　　　　运行耗时(分钟),　等待耗时(分钟)"
    increaseTask = []
    for index, row in df.iterrows():
        name = row['name']
        if name not in taskNameList:
            task_start_time = row['start_time']
            task_end_time = row['end_time']
            process_time = row['process_time']
            waiting_time = row['waiting_time']
            task_detail = ',　'.join([name, str(task_start_time)[6:].replace(' ','_'), str(task_end_time)[6:].replace(' ','_'), str(int(process_time/60)), str(int(waiting_time/60))])
            ding_text = ding_text + "\\n" + task_detail
            increaseTask.append(name)

    ding_text = ding_text.replace(' ', '') + "\\n"
    print(increaseTask)
    print(ding_text)
    if increaseTask:
        os.system('sh /home/hadoop/alarm/ding/ding2.sh "通知:{ding_text}"'.format(ding_text=ding_text))