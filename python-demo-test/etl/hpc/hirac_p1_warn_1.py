## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: hirac 8-9点任务堆积告警
#---------
import requests
import re
import os
import time



hirac_url = "http://hirac.yangtuojia.com/metrics"
res_code = None
metric_result = None
ding_text = None


while res_code != 200:
    responce = requests.get(hirac_url,params={}, headers = {'Content-type': 'text/plain; version=0.0.4;charset=utf-8','Accept': '*/*'})
    res_code = responce.status_code
    if res_code == 200:
        metric_result = str(responce.content, encoding = "utf-8")
        break
    else:
        time.sleep(5)


print(metric_result)

searchObj = re.search( r'waiting_job_inQueue{queue="离线",} (\d.*?)', metric_result, re.M|re.I)


if searchObj:
    print("searchObj.group() : ", searchObj.group())
    waiting_task_num = int(searchObj.group(1))
    print(waiting_task_num)
    if waiting_task_num >= 0 :
        ding_text = "离线任务(7-9/d)等待队列阀值监控通知\n  当前值：{waiting_task_num}个 \n  状态: 超过设定阀值250".format(waiting_task_num=waiting_task_num)
        print(ding_text)
        os.system('sh /home/hadoop/alarm/ding/ding1.sh "通知:{ding_text}"'.format(ding_text=ding_text))
else:
    print("Nothing found!!")
