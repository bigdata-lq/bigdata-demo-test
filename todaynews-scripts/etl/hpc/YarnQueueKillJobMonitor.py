# -*-coding:utf-8 -*-
# ---------
# Name:lq
# Message: 清除任务耗时过长的任务
# ---------

import requests
import json
import time

killYarnJobUrl = "http://prod-hadoop-master001:8088/ws/v1/cluster/apps/{applicationId}/state"
getRunningYarnJobUrl = "http://prod-hadoop-master001:8088/ws/v1/cluster/apps?queue={queueName}&states=RUNNING&limit=500"



def getYarnJobByQueueName(queueName) :
    responce = requests.get(url = getRunningYarnJobUrl.format(queueName = queueName),
                            headers = {"Content-Type":"application/json"})

    appList = responce.json()["apps"]
    if appList is None:
        return None
    print(len(appList["app"]))
    return appList


def killYarnJobByApplicationId(applicationId):
    ## KILL ApplicationId
    res = requests.put(url = killYarnJobUrl.format(applicationId = applicationId),
                 headers = {"Content-Type":"application/json"},
                       data = json.dumps({"state":"KILLED"}))
    print(res)
    return res.status_code


if __name__ == '__main__':

    queuelist = ["root.P2.common", "root.P0","root.users.hadoop","root.users.readonly"]
    for queue in queuelist:
        print("----------------{queue}-----------------".format(queue=queue))
        appList = getYarnJobByQueueName(queue)
        if appList:
            for appJson in appList["app"]:
                diff_time = time.time()-appJson['startedTime']/1000
                if diff_time > 5*3600: # 运行超过5h
                    print('任务已启动超过{diff_time}秒,applicationId为{id},准备kill掉'.format(diff_time=diff_time, id=appJson['id']))
                    res = killYarnJobByApplicationId(appJson['id'])
                    print("----------------kill applicationId: {applicationId}-----------------responceCode is: {res}-----------------".format(applicationId = appJson['id'],res = res))