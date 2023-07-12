## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 离线任务异常值监控
#---------
import sys
import pymysql
import pandas as pd
params = sys.argv


## meta jdbc参数信息
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
        mysql_client = pymysql.connect(**databaseInfo)
        df = pd.read_sql(sql, mysql_client)
        df.fillna("", inplace=True)
        mysql_client.close()
        return df

# 离线任务近14天运行时间 去除一天运行多次和运行不足15天
job_success_process_sql = """

select 
		job_name,
		
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 0 DAY), '%Y-%m-%d'),process_time,0)) AS before_0day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 1 DAY), '%Y-%m-%d'),process_time,0)) AS before_1day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 2 DAY), '%Y-%m-%d'),process_time,0)) AS before_2day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 3 DAY), '%Y-%m-%d'),process_time,0)) AS before_3day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 4 DAY), '%Y-%m-%d'),process_time,0)) AS before_4day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 5 DAY), '%Y-%m-%d'),process_time,0)) AS before_5day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 6 DAY), '%Y-%m-%d'),process_time,0)) AS before_6day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 7 DAY), '%Y-%m-%d'),process_time,0)) AS before_7day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 8 DAY), '%Y-%m-%d'),process_time,0)) AS before_8day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 9 DAY), '%Y-%m-%d'),process_time,0)) AS before_9day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 10 DAY), '%Y-%m-%d'),process_time,0)) AS before_10day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 11 DAY), '%Y-%m-%d'),process_time,0)) AS before_11day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 12 DAY), '%Y-%m-%d'),process_time,0)) AS before_12day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 13 DAY), '%Y-%m-%d'),process_time,0)) AS before_13day_process_time,
		SUM(IF(start_time = date_format(DATE_SUB(NOW(),INTERVAL 14 DAY), '%Y-%m-%d'),process_time,0)) AS before_14day_process_time
from 
(
		select 
				j.name job_name, 
				date_format(h.start_time, '%Y-%m-%d') as start_time, 
				TIMESTAMPDIFF(SECOND,h.start_time,h.end_time) process_time,
				TIMESTAMPDIFF(SECOND,h.gmt_create,h.start_time) waiting_time
		from hera_job j
		left join 
		hera_action_history h
		on j.id = h.job_id
		where  j.auto = 1
		and    h.gmt_create > DATE_SUB(NOW(),INTERVAL 15 DAY) and h.gmt_create < date_add(NOW(), INTERVAL 15 DAY)
		and    j.name not like 'dqc%' 
		and    h.is_nrt = 0 -- 0离线，1准实时
		and    h.trigger_type = 1 -- 1自动调度, 2手动触发, 3手动恢复
		and    h.status='success'
) t1 group by job_name HAVING count(1) = 15 limit 1

"""

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

df = MysqlUtil.read_myql("hirac",job_success_process_sql)

# 基于箱型图的异常值检测
for i,r in df.iterrows():
    print(r)
    job_name = r['job_name']
    data_y = pd.Series([
        r['before_0day_process_time'], r['before_1day_process_time'], r['before_2day_process_time'], r['before_3day_process_time'],
        r['before_4day_process_time'], r['before_5day_process_time'], r['before_6day_process_time'], r['before_7day_process_time'],
        r['before_8day_process_time'], r['before_9day_process_time'], r['before_10day_process_time'], r['before_11day_process_time'],
        r['before_12day_process_time'], r['before_13day_process_time'], r['before_14day_process_time']])
    statistics = data_y.describe(percentiles=[.75, .25]) #保存基本统计量
    print(statistics)
    IQR = statistics.loc['75%']-statistics.loc['25%']   #四分位数间距
    QL = statistics.loc['25%']  #下四分位数
    QU = statistics.loc['75%']  #上四分位数
    threshold1 = QL - 1.5 * IQR #下阈值
    threshold2 = QU + 1.5 * IQR #上阈值

    outlier = [] #将异常值保存

    for i in range(0, len(data_y)):
        if (data_y[i] < threshold1)|(data_y[i] > threshold2):
            outlier.append(data_y[i])
        else:
            continue

    print('\n异常数据如下：\n')
    print(outlier)