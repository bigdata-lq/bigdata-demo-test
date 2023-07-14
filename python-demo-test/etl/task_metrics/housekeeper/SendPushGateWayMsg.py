## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 1.发送yt_edp流任务监控指标到pushgateaWay
# 入参 downstream ytdw dw_order_d order_id
#---------

import requests
import json
import pandas as pd
import schedule
import threading
import time

class JobUtil(object):

    @staticmethod
    def sendPushGateway(url, dimensions, job_name, metric_name, metric_value):
        r"""
        :param url: stream/task/list
        :param dimensions: dim
        :param job_name:
        :param metric_name: 指标key
        :param metric_value: 指标value
        :return:
        """
        headers = {'X-Requested-With': 'Python requests', 'Content-type': 'text/xml'}
        dim = ''
        for key in dimensions.keys():
            dim += '/%s/%s' % (key, dimensions[key])
        try:
            r = requests.post('http://%s/metrics/job/%s%s' % (url, job_name, dim),
                  data='# TYPE %s gauge\n%s %s\n' % (metric_name,metric_name, metric_value), headers=headers, timeout=(60,600))
            r.raise_for_status() # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            print(e)


    @staticmethod
    def getHopUrlRes(url, param):
        r"""
        :param url:
        :param param:
        :return:
        """
        url = "https://edp.yangtuojia.com/" + url
        headers={
            'Content-Type':'application/json;charset=UTF-8'
        }
        try:
            r = requests.post(url, data=json.dumps(param), headers = headers, timeout=(60,600))
            r.raise_for_status()
        except requests.RequestException as e:
            print(e)
            return
        return json.loads(r.text).get("data",None)




def sendTaskJobNumMetric(url, job_name, task_list):
    r"""
    :param task_list:
    :return:
    """
    task_df = pd.DataFrame.from_dict(task_list, orient='columns')
    print("print task job num metric....")
    ## 任务数指标
    task_group = task_df.groupby(["type","status"])
    task_num_df = task_group.size().reset_index(name='num')
    print(task_num_df)
    # task_df2 = task_group['name'].apply(lambda x:x.str.cat(sep=',')).reset_index()
    # print(task_df2)
    for index, row in task_num_df.iterrows():
        job_num_metric_name = "flink_job_num_prod"
        job_num_metric_value = row["num"]
        job_num_dimensions = {"instance":"edp-flink"}
        ## running stop
        if row["status"] == 0:
            job_num_dimensions['job_status']= "未开始"
        elif row["status"] == 1:
            job_num_dimensions['job_status']= "运行中"
        elif row["status"] == 2:
            job_num_dimensions['job_status']= "停止"
        else:
            job_num_dimensions['job_status']= "失败"

        if row["type"] == 1:
            job_num_dimensions['job_type'] = "预处理任务"
        else:
            job_num_dimensions['job_type'] = "SQL任务"
        # job_num_dimensions['job_name'] = row["name"]
        JobUtil.sendPushGateway(url, job_num_dimensions, job_name, job_num_metric_name, job_num_metric_value)

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def sendTaskJobOffsetMetric(url, job_name, task_list):
    r"""
    :param task_list:
    :return:
    """
    ## 任务offset指标
    metricOffsetIsOverDetailList = []
    for task in task_list:
        if task.get("totalLag") and task.get("thresholdOpen") == 1 and task.get("thresholdAlarm") and task.get("totalLag") > task.get("thresholdAlarm"):
            job_offset_metric_name = "flink_job_offset_over_detail_prod"
            job_offset_metric_value = task.get("totalLag") - task.get("thresholdAlarm")
            if job_offset_metric_value > 0:
                ## 超出offset任务信息
                job_offset_dimensions = {"instance":"edp-flink"}
                ## 预处理 sql计算
                if task.get("type") == 1:
                    job_offset_dimensions['job_type'] = "预处理任务"
                    metricOffsetIsOverDetailList.append(["预处理任务","超过阈值",task.get("name")])
                else:
                    job_offset_dimensions['job_type'] = "SQL任务"
                    metricOffsetIsOverDetailList.append(["SQL任务","超过阈值",task.get("name")])
                job_offset_dimensions['job_name'] = task.get("name")
                JobUtil.sendPushGateway(url, job_offset_dimensions, job_name, job_offset_metric_name, job_offset_metric_value)
        else :
            if task.get("type") == 1:
                metricOffsetIsOverDetailList.append(["预处理任务","正常阈值",task.get("name")])
            else:
                metricOffsetIsOverDetailList.append(["SQL任务","正常阈值",task.get("name")])
    metricOffsetIsOverDF = pd.DataFrame(metricOffsetIsOverDetailList, columns=['type', 'isNormal', 'name'])
    metricOffsetIsOverNumDF = metricOffsetIsOverDF.groupby(["type","isNormal"]).size().reset_index(name='num')

    for index, row in metricOffsetIsOverNumDF.iterrows():
        job_offset_over_num_metric_name = "flink_job_offset_over_num_prod"
        job_offset_over_num_metric_value = row["num"]
        job_offset_over_num_dimensions = {"instance":"edp-flink"}
        job_offset_over_num_dimensions['job_type'] = row["type"]
        job_offset_over_num_dimensions['isNormal'] = row["isNormal"]
        JobUtil.sendPushGateway(url, job_offset_over_num_dimensions, job_name, job_offset_over_num_metric_name, job_offset_over_num_metric_value)


def sendTaskJobMetric():
    ## 任务信息
    edp_task_url = "stream/task/list"
    param = {
        "pageSize":2000,
        "pageNo": 1
    }
    task_list = JobUtil.getHopUrlRes(edp_task_url, param)
    if task_list is None:
        return
    url = '10.100.7.138:9091'
    job_name = "yt_edp_flink_metric"
    sendTaskJobOffsetMetric(url, job_name, task_list)
    sendTaskJobNumMetric(url, job_name, task_list)


if __name__ == '__main__':
    report_interval = 10
    ## 定时器 异步处理
    schedule.every(report_interval).seconds.do(sendTaskJobMetric)
    # schedule.every(report_interval).seconds.do(run_threaded,sendTaskJobOffsetMetric(url, job_name, task_list))

    while True:
        schedule.run_pending()
        time.sleep(1)











