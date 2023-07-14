## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 离线任务异常值监控
#---------
import sys
import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #导入绘图库
params = sys.argv
import time
import json


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



class Utils(object):

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

    def getOutliers(sc_df, job_name, index_name):
        """
        count     14.000000 计数
        mean     374.642857 平局值
        std       97.136389 标准差
        min      262.000000 最小值
        25%      312.250000 1/4位数
        50%      361.000000 中位数
        75%      405.500000 3/4位数
        max      660.000000 最大数
        :param job_name: 任务名
        :return:
        """

        ## 行转列
        df = sc_df.pivot_table(index=['start_time'],
                               columns='job_name',
                               values=index_name
                               ).reset_index()
        data_y = df[job_name]
        # df[u'start_time']
        # scale_ls = range(14)
        data_x = df[u'start_time']
        statistics = data_y.describe() #保存基本统计量
        mean = statistics['mean']
        IQR = statistics.loc['75%']-statistics.loc['25%']   #四分位数间距
        QL = statistics.loc['25%']  #下四分位数
        QU = statistics.loc['75%']  #上四分位数
        threshold1 = QL - 1.5 * IQR #下阈值
        threshold2 = QU + 2.0 * IQR #上阈值
        outlier = [] #将异常值保存
        outlier_x = []

        if mean > 720 : ##30天均值破15分钟
            for i in range(0, len(data_y)):
                if data_y[i] > threshold2:
                    outlier.append((job_name, data_x[i], data_y[i]))
                    # outlier_x.append(scale_ls[i])
                else:
                    continue
            if len(outlier) > 0:
                for i in outlier:
                    if i[1] == now_day:
                        print(sc_df)
                        print(statistics)
                        print('\n{job_name}:异常数据如下:'.format(job_name = job_name))
                        process_res.append(i)
                        print(i)
                        print('-----------------------------分界线-分界线-------------------------------')

        return outlier

# 离线任务近14天运行时间
job_success_process_sql = """
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
		and    h.gmt_create > DATE_SUB(NOW(),INTERVAL 30 DAY) and h.gmt_create < date_add(NOW(), INTERVAL 1 DAY)
		and    j.name not like 'dqc%' 
		and    h.is_nrt = 0 -- 0离线，1准实时
		and    h.trigger_type = 1 -- 1自动调度, 2手动触发, 3手动恢复
		and    h.status='success' 
		and    j.name in ('{job_name}')

"""
job_sql = """
    select 
        distinct j.name as job_name
		from hera_job j
		left join 
		hera_action_history h
		on j.id = h.job_id
    where  j.auto = 1
		and    h.gmt_create >= date_format(NOW(), '%Y-%m-%d') and h.gmt_create < date_add(NOW(), INTERVAL 1 DAY)
		and    j.name not like 'dqc%' 
		and    h.is_nrt = 0 -- 0离线，1准实时
		and    h.trigger_type = 1 -- 1自动调度, 2手动触发, 3手动恢复
		and    h.status='success'  
		and    TIMESTAMPDIFF(SECOND,h.start_time,h.end_time) > 720
"""

job_conf_sql = """
    select configs from hera_job where name = '{job_name}'
"""

if __name__ == '__main__':

    pd.set_option('display.max_rows',500)
    pd.set_option('display.max_columns',6000)
    pd.set_option('display.width',10000)

    now_day = time.strftime("%Y-%m-%d", time.localtime())

    job_df = Utils.read_myql("hirac",job_sql)
    process_res = []
    for index, row in job_df.iterrows():
        job_name = row['job_name']
        sc_df = Utils.read_myql("hirac",job_success_process_sql.format(job_name = job_name))
        outlier = Utils.getOutliers(sc_df, job_name, "process_time")


    print('-----------------------------今日破线任务-------------------------------')

    for i in process_res:
        conf_df = Utils.read_myql("hirac",job_conf_sql.format(job_name = i[0]))
        conf = conf_df['configs'][0]
        print(json.loads(conf)['run.priority.level'])
        print(conf)






