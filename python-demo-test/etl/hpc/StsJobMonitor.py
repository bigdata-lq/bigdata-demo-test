## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 监控sts是否存活
#---------

import requests
import json
import os

stsJobUrl = "http://prod-hadoop-master001:8088/ws/v1/cluster/apps?queue={queueName}"

stsJobList = ['prod-sts001 ThriftServer', 'prod-sts003 ThriftServer', 'prod-sts005 ThriftServer', 'prod-sts006 ThriftServer ', 'prod-sts007 ThriftServer', 'prod-sts008 ThriftServer']

ding_text = '{name}　is　down　!!!!'

def getYarnJobByQueueName(queueName):
    responce = requests.get(url = stsJobUrl.format(queueName = queueName),
                            headers = {"Content-Type":"application/json"})

    appList = responce.json()["apps"]
    return appList


if __name__ == '__main__':

    print("----------------root.adhoc-----------------")
    appList = getYarnJobByQueueName("root.adhoc")

    runningApp = []
    for application in appList['app']:
        if application['state'] == 'RUNNING' :
            runningApp.append(application['name'].strip())

    res = list(set(stsJobList)-set(runningApp))
    if len(res) > 0:
        ding_text = ding_text.format(name = ','.join(res)).replace(" ", "　")
        print(ding_text)
        print(len(res))
        # os.system('sh /home/hadoop/alarm/ding/ding2.sh "通知:{ding_text}"'.format(ding_text=ding_text))

    for host in res:
        script = 'sh /home/hadoop/alarm/sts/startSingleSTS.sh {host}'.format(host = host.split(" ")[0])
        print(script)
        os.system(script)