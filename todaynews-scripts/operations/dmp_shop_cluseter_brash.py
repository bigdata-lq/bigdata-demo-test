import requests
import json
import os
import time

dmp_domain = "https://20220706-octopus-bug-dmpapi.yangtuojia.com"
# dmp_domain = "https://pre-dmpapi.yangtuojia.com"

getNeedBrushClusterIdListUrl = "{dmp_domain}/getNeedBrushClusterIdList"
getShopClusterSyncToCrmScript = "{dmp_domain}/getShopClusterSyncToCrmScript?id={clusterId}"
startTime = time.time()


class RequestApi(object):

    @staticmethod
    def api_post(url, param):
        # headers 定义
        headers = {"Content-Type":"application/json"}
        return requests.post(url, headers=headers, json=param).json()

    @staticmethod
    def api_get(url, param):
        # headers 定义
        headers = {"Content-Type":"application/json"}
        return requests.get(url, headers=headers, params=param)



needBrushClusterIdListUrl = getNeedBrushClusterIdListUrl.format(dmp_domain = dmp_domain)
clusterIdListRes = json.loads(RequestApi.api_get(needBrushClusterIdListUrl,None).content.decode())
print("{time} :Start Refresh dmp task ............".format(time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
clusterIdList = clusterIdListRes['data']
print("获取需要重刷的圈选ID LIST : {clusterIdStr}" .format(clusterIdStr = ','.join([str(x) for x in clusterIdList])))

## 临时测试数据
clusterIdList = [455]
if clusterIdListRes['code'] == '200' and len(clusterIdList) > 0 :
    for clusterId in clusterIdList:
        ## 获取需要重刷的圈选ID的Script
        print("Start---Start重刷圈选ID为 {clusterId}的任务" .format(clusterId = clusterId))
        shopClusterSyncToCrmScriptUrl = getShopClusterSyncToCrmScript.format(dmp_domain = dmp_domain, clusterId = clusterId)
        clusterScriptRes = json.loads(RequestApi.api_get(shopClusterSyncToCrmScriptUrl, None)
                                   .content.decode())
        clusterScript = clusterScriptRes['data']
        fileName = str(clusterId) + "-" + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time())) + ".log"

        if clusterScriptRes['code'] == '200' and len(clusterScript) > 0 :
            clusterScript = clusterScript + ' > /alidata/workspace/yt_bigdata/edp/dmp_shop_cluster/log/{fileName}'.format(fileName = fileName)
            print("clusterId is {clusterId} , clusterScript is {clusterScript} ".format(clusterId = clusterId, clusterScript = clusterScript))
            # os.system(clusterScript)
            print("End---End重刷圈选ID为 {clusterId}的任务, 耗时{runningTime}分钟" .format(clusterId = clusterId, runningTime = (time.time() - startTime)/60))
        else:
            print("ERROR url:"+ shopClusterSyncToCrmScriptUrl + " request is exception or result is empty")
        print("----------------------------------------------------------------------------------------------------------")

else:
    print("WARN url:"+ needBrushClusterIdListUrl + " request is exception or result is empty")
