from operations.request_util import RequestApi
import json
import datetime
from operations.mysql_util import MysqlUtil

## 维度权重信息
dim_base_detail = {
    ## 存储 (均衡度, 阀值1, 阀值2, 维度中文名)
    "vcore_total_num" :(0,None,None,"Vcore总数"),
    "memory_totol_num" : (0,None,None,"Memory总数"),
    "compute_total_node" :(0,None,None,"计算节点"),
    "unhealthy_node_num": (20,1,2, '计算节点宕机数'),
    "vcore_used_rate": (10,90,60, 'vcore使用率'),

    "vcore_pending_rate" : (20,0,5, 'vcorePending占比'),

    "memory_used_rate" : (10,90,60, 'memory使用率'),
    "memory_pending_rate":(20,0,5, 'memoryPending占比')
}

yarn_jmx_url = "http://prod-hadoop-master001:8088/ws/v1/cluster/metrics"


## 存储健康大盘
board_code = "compute_health_tray"
board_overview_code = "compute_overview_health_tray"

componentHealthFields = ['board_code','dim_name', 'dim_status','dim_value', 'expect_score', 'actual_score', 'weight', 'weight_percent', 'health_detail', 'collect_time']
componentHealthValues = []
collect_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
collect_time_hour = datetime.datetime.now().strftime('%H')
before_30_time = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')


## 计算情况概览
def compute_overview(metrics,dim_key):
    dim_name = dim_base_detail[dim_key][3]
    if dim_key == 'vcore_total_num':
        dim_value = metrics['totalVirtualCores']
    if dim_key == 'memory_totol_num':
        dim_value = metrics['totalMB']
    if dim_key == 'compute_total_node':
        dim_value = metrics['totalNodes']

    componentHealthValues.append((board_overview_code, dim_name, None, dim_value, None, None, None, None, None, collect_time))
    return (board_overview_code, dim_name, None, dim_value, None, None, None, None, None, collect_time)

## 健康分维度
def compute_dim_score(metrics, dim_key):

    ## 存储节点宕机数
    dim_name = dim_base_detail[dim_key][3]
    dim_value = None
    health_detail = None
    dim_status = None
    status_percent = None

    if dim_key == 'unhealthy_node_num':
        dim_value = metrics['unhealthyNodes']
        health_detail = '计算节点发生跌机，详细信息：{dim_value},请修复！'.format(dim_value = str(dim_value))
    elif dim_key == 'vcore_used_rate':
        dim_value = round((metrics['reservedVirtualCores'] + metrics['allocatedVirtualCores'])/ metrics['totalVirtualCores'],5) * 10
    elif dim_key == 'vcore_pending_rate':
        dim_value = round(metrics['containersPending'] * 2 / metrics['totalVirtualCores'])
    elif dim_key == 'memory_used_rate':
        dim_value = round((metrics['reservedMB'] + metrics['allocatedMB']) / metrics['totalMB'],5) * 100
    elif dim_key == 'memory_pending_rate':
        dim_value = round(metrics['containersPending'] * 1024 / metrics['totalMB'])

    weight = dim_base_detail[dim_key][0]
    weightTotal = 0
    for value in dim_base_detail.values():
        weightTotal += value[0]
    weight_percent = round(dim_base_detail[dim_key][0]/ weightTotal,5)
    if dim_key in ['vcore_pending_rate', 'memory_pending_rate']:
        if dim_value <= dim_base_detail[dim_key][1]:
            status_percent = 1
            dim_status = "GOOD"
        elif dim_value >= dim_base_detail[dim_key][2]:
            status_percent = 0.8
            dim_status = "BAD"
            health_detail = '{dim_name}等待率超过最大阀值{dim_value}%,请加大资源！！'.format(dim_name = dim_name, dim_value = dim_base_detail[dim_key][2])
        else:
            status_percent = 0.6
            dim_status = "CONCERNING"
            health_detail = '{dim_name}等待率超过阀值{dim_value}%,请加大资源！'.format(dim_name = dim_name, dim_value = dim_base_detail[dim_key][1])
    elif dim_key == 'vcore_used_rate' or dim_key =='memory_used_rate':
        value_limit = None
        if int(collect_time_hour) < 10 :
            value_limit = dim_base_detail[dim_key][1]
        else:
            value_limit = dim_base_detail[dim_key][2]

        if dim_value > dim_base_detail[dim_key][1]:
            status_percent = 1
            dim_status = "GOOD"
            health_detail = None
        else:
            status_percent = 0.8
            dim_status = "CONCERNING"
            health_detail = '{dim_name}使用率不高,还存在资源空闲,可以适当加大调度并行度'.format(dim_name = dim_name)
    else:
        if dim_value <= dim_base_detail[dim_key][1]:
            status_percent = 1
            dim_status = "GOOD"
        elif dim_value >= dim_base_detail[dim_key][2]:
            status_percent = 0.8
            dim_status = "BAD"
        else:
            status_percent = 0.6
            dim_status = "CONCERNING"

    if dim_status == "GOOD" :
        health_detail = None


    expect_score = round(100 * weight_percent,4)

    actual_score = round(100 * weight_percent * status_percent,4)

    componentHealthValues.append((board_code, dim_name, dim_status, dim_value, expect_score, actual_score, weight, weight_percent, health_detail, collect_time))
    return (board_code, dim_name, dim_status, dim_value, expect_score, actual_score, weight, weight_percent, health_detail, collect_time)




if __name__ == '__main__':

    ##YARN监控相关信息
    response = RequestApi.api_get(yarn_jmx_url, sessionId=None, param=None)

    compute_metrics = eval(response.content.decode())['clusterMetrics']


    vcore_total_num = compute_overview(compute_metrics, 'vcore_total_num')
    memory_totol_num = compute_overview(compute_metrics, 'memory_totol_num')
    compute_total_node = compute_overview(compute_metrics, 'compute_total_node')


    unhealthy_node_num = compute_dim_score(compute_metrics, 'unhealthy_node_num')
    vcore_used_rate = compute_dim_score(compute_metrics, 'vcore_used_rate')
    vcore_pending_rate = compute_dim_score(compute_metrics, 'vcore_pending_rate')
    memory_used_rate = compute_dim_score(compute_metrics, 'memory_used_rate')
    memory_pending_rate = compute_dim_score(compute_metrics, 'memory_pending_rate')

    print(componentHealthValues)
    MysqlUtil.insert_batch("meta", "cluster_dim_health_check_info", componentHealthFields, componentHealthValues)

    ##删除1个月以前数据
    delete_sql = "delete from cluster_dim_health_check_info where board_code = '{board_code}' and create_time < '{create_time}'" \
        .format(board_code=board_code,create_time = before_30_time)
    print(delete_sql)
    MysqlUtil.excuse("meta", delete_sql)

    delete_sql = "delete from cluster_dim_health_check_info where board_code = '{board_code}' and create_time < '{create_time}'" \
        .format(board_code=board_overview_code,create_time = before_30_time)
    print(delete_sql)
    MysqlUtil.excuse("meta", delete_sql)
