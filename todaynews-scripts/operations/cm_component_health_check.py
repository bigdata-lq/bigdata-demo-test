import requests
from requests.auth import HTTPDigestAuth, HTTPBasicAuth

from operations.request_util import RequestApi
import json
import datetime
from operations.mysql_util import MysqlUtil

## 账号密码
username = 'cm_readonly'
password = 'hipac001'

## login
login_url = 'http://cm.yangtuojia.com:7180/api/v18/clusters/hcluster'
## 服务状态
service_url = 'http://cm.yangtuojia.com:7180/api/v18/clusters/hcluster/services'
## healthCheck
healthCheck_Formaturl = "http://cm.yangtuojia.com:7180/cmf/services/{serviceId}/healthCheck.json?timestamp={time}&currentMode=true&_={time}"

## 服务编号
service_dict = {
    "hdfs": 6, "hbase": 14, "hive": 12, "yarn": 8, "zookeeper": 4
}

## 维度权重信息
dim_weight = {
    ## Hdfs
    "HDFS_FAILOVER_CONTROLLERS_HEALTHY": 10,
    "HDFS_HA_NAMENODE_HEALTH": 10,
    "HDFS_DATA_NODES_HEALTHY" : 8,

    ## HBASE
    "HBASE_MASTER_HEALTH": 8,
    "HBASE_REGION_SERVERS_HEALTHY" : 5,

    ## HIVE
    "HIVE_HIVEMETASTORES_HEALTHY" : 10,
    "HIVE_HIVESERVER2S_HEALTHY" : 5,

    # Zookeeper
    "ZOOKEEPER_SERVERS_HEALTHY" : 10,

    ## Yarn
    "YARN_JOBHISTORY_HEALTH" : 5,
    "YARN_NODE_MANAGERS_HEALTHY": 8,
    "YARN_RESOURCEMANAGERS_HEALTH" : 10
}

## 维度名称
dim_name_dict = {
    ## Hdfs
    "HDFS_FAILOVER_CONTROLLERS_HEALTHY": "Failover Controller",
    "HDFS_HA_NAMENODE_HEALTH": "NameNode",
    "HDFS_DATA_NODES_HEALTHY" : "DataNode",

    ## HBASE
    "HBASE_MASTER_HEALTH": "HMaster",
    "HBASE_REGION_SERVERS_HEALTHY" : "HRegion",

    ## HIVE
    "HIVE_HIVEMETASTORES_HEALTHY" : "HiveMetaStore",
    "HIVE_HIVESERVER2S_HEALTHY" : "HiveServer2",

    # Zookeeper
    "ZOOKEEPER_SERVERS_HEALTHY" : "Zookeeper",

    ## Yarn
    "YARN_JOBHISTORY_HEALTH" : "YJobHistory",
    "YARN_NODE_MANAGERS_HEALTHY": "YNodeManager",
    "YARN_RESOURCEMANAGERS_HEALTH" : "YResourceManager"
}


## 状态得分率
status_score_percent = {
    "GOOD": 1.0,
    "CONCERNING" : 0.8,
    "BAD" : 0.6
}

## 组件监控大盘Code
board_code = "component_health_tray"


if __name__ == '__main__':

    componentHealthFields = ['board_code','dim_name', 'dim_status', 'expect_score', 'actual_score', 'weight', 'weight_percent', 'health_detail', 'collect_time']
    componentHealthValues = []
    ##获取sessionId
    sessionId = RequestApi.get_cookies(login_url, username, password)

    ##获取服务状态信息
    response = RequestApi.api_get(service_url, sessionId=sessionId, param=None)

    itemsList = json.loads(response.content.decode())['items']
    collect_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    before_30_time = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
    for item in itemsList:
        itemName = item["name"]
        healthChecks = item["healthChecks"]
        healthSummary = item["healthSummary"]
        healthSummaryDetail = {}

        if itemName in service_dict.keys():
            ## 健康检查
            serviceId = service_dict[itemName]

            healthCheckUrl = healthCheck_Formaturl.format(serviceId = serviceId, time = int(round(datetime.datetime.now().timestamp() * 1000)))

            res = RequestApi.api_get(healthCheckUrl, sessionId=sessionId, param=None)
            healthSummaryList = json.loads(res.content.decode())['data']['healthReport']['testResults']

            for healthSummaryDict in healthSummaryList:
                healthSummaryDetail[healthSummaryDict['testName']] = healthSummaryDict['explanation']


        for healthCheck in healthChecks :

            dim_name_key = healthCheck['name']

            if dim_name_key in dim_weight.keys():
                health_detail = None
                dim_name = dim_name_dict[dim_name_key]
                dim_value = healthCheck['summary']
                weight = dim_weight[dim_name_key]
                weight_percent = round(weight/ sum(dim_weight.values()),5)
                status_percent = status_score_percent[dim_value]
                expect_score = round(100 * weight_percent,4)
                actual_score = round(100 * weight_percent * status_percent,4)
                if len(healthSummaryDetail) > 0 :
                    health_detail = healthSummaryDetail[dim_name_key]
                componentHealthValues.append((board_code, dim_name, dim_value, expect_score, actual_score, weight, weight_percent, health_detail, collect_time))
                # print((dim_name, dim_value, expect_score, actual_score, weight, weight_percent, health_detail, collect_time))

    print(componentHealthValues)
    MysqlUtil.insert_batch("meta", "cluster_dim_health_check_info", componentHealthFields, componentHealthValues)

    ##删除1个月以前数据
    delete_sql = "delete from cluster_dim_health_check_info where board_code = '{board_code}' and create_time < '{create_time}'"\
        .format(board_code=board_code,create_time = before_30_time)
    print(delete_sql)
    MysqlUtil.excuse("meta", delete_sql)
