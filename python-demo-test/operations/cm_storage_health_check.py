from operations.request_util import RequestApi
import json
import datetime
from operations.mysql_util import MysqlUtil

## 维度权重信息
dim_base_detail = {
    ## 存储 (均衡度, 阀值1, 阀值2, 维度中文名)
    "hdfs_total_storage" :(0,None,None,"hdfs存储总容量"),
    "storage_file_num" :(0,None,None,"存储文件总数"),
    "storage_block_num" : (0,None,None,"存储block总数"),
    "storage_total_node" :(0,None,None,"存储节点总数"),
    "dead_node_num": (10,1,2, '存储节点宕机数'),
    "vol_fail_num": (10,1,3, '坏盘数量'),

    "storage_balance_rate" : (8,4,8, '存储数据均衡度'),

    "hdfs_block_missing_rateHDFS" : (5,0.1,1, '数据丢失率'),
    "bad_block_num":(5,20,100, '坏块数量'),
    "hdfs_file_num": (5, 16000000, 2000000, 'HDFS小文件数量'),

    "hdfs_storage_rate": (20,65,70, 'HDFS存储使用率'),
    "storage_rate_less70_node_rate": (20, 30, 60, '存储率大于70%节点占比')
}

hdfs_jmx_url = "http://prod-hadoop-master001:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"


## 存储健康大盘
board_code = "storage_health_tray"
board_overview_code = "storage_overview_health_tray"

componentHealthFields = ['board_code','dim_name', 'dim_status','dim_value', 'expect_score', 'actual_score', 'weight', 'weight_percent', 'health_detail', 'collect_time']
componentHealthValues = []
collect_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
before_30_time = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
false = False
true = True


## 计算情况概览
def compute_overview(metrics,dim_key):
    dim_name = dim_base_detail[dim_key][3]
    if dim_key == 'hdfs_total_storage':
        dim_value = metrics['Total']
    if dim_key == 'storage_file_num':
        dim_value = metrics['TotalFiles']
    if dim_key == 'storage_block_num':
        dim_value = metrics['TotalBlocks']
    if dim_key == 'storage_total_node':
        dim_value = len(eval(metrics['LiveNodes'])) + len(eval(namenodeInfo["DeadNodes"]))

    componentHealthValues.append((board_overview_code, dim_name, None, dim_value, None, None, None, None, None, collect_time))
    return (board_overview_code, dim_name, None, dim_value, None, None, None, None, None, collect_time)


def compute_dim_score(namenodeMetrics, dim_key):

    ## 存储节点宕机数
    dim_name = dim_base_detail[dim_key][3]
    dim_value = None
    health_detail = None
    dim_status = None
    status_percent = None

    if dim_key == 'dead_node_num' :
        dim_value = len(eval(namenodeInfo["DeadNodes"]))
        health_detail = "存储节点发生跌机,详细信息：" + str(namenodeInfo["DeadNodes"])
    elif dim_key == 'vol_fail_num' :
        dim_value = 0

        ## 坏盘个数
        vol_fail_detail = eval(namenodeInfo["LiveNodes"]).values()
        hostList = []
        for value in vol_fail_detail:
            volfails = value['volfails']
            dim_value += volfails
            if volfails >= 0 :
                hostList.append(value['infoAddr'].split(":")[0])

        ## 坏盘机器IP
        if len(hostList) > 0 :
            health_detail = "集群机器有磁盘损坏,坏盘IP为:" + "_".join(hostList) + ",请进联系运维进行修复！"
    elif dim_key == 'storage_balance_rate' :
        ##存储标准差
        dim_value = float(eval(namenodeInfo["NodeUsage"])['nodeUsage']['stdDev'].replace("%",""))
        health_detail = "集群block块存储不均衡, 存储标准差高于5%, 均衡详细指标为:" + str(eval(namenodeInfo["NodeUsage"])['nodeUsage'])

    elif dim_key == 'hdfs_block_missing_rateHDFS':
        ##数据丢失率
        dim_value = round(namenodeInfo["NumberOfMissingBlocks"]/namenodeInfo["TotalBlocks"],5)*100
        health_detail = None
    elif dim_key == 'bad_block_num':
        ##坏文件数量
        dim_value = len(eval(namenodeInfo["CorruptFiles"]))
        health_detail = "集群存在损坏的数据块,详细信息为："+ " ".join(str(eval(namenodeInfo["CorruptFiles"])) + ",请修复")

    elif dim_key == 'hdfs_file_num':
        ##小文件数量
        dim_value = namenodeInfo["TotalFiles"]
        if dim_value > dim_base_detail[dim_key][1] :
            health_detail = "集群小文件数量超过阈值{dim_value},NameNode压力过大，请开启小文件合并！！".format(dim_value=dim_base_detail[dim_key][1])

    elif dim_key == "hdfs_storage_rate":
        dim_value = namenodeInfo['PercentUsed']
        if dim_value > dim_base_detail[dim_key][1] :
            health_detail = "HDFS存储平均使用率超过阈值{dim_value}%,请及时处理！！".format(dim_value=dim_base_detail[dim_key][1])

    elif dim_key == "storage_rate_less70_node_rate":
        dim_value = 0
        storage_rate_less70_num = 0
        all_value = len(eval(namenodeInfo["LiveNodes"]).values())
        storage_rate_less70_node_detail = eval(namenodeInfo["LiveNodes"]).values()
        hostList = []
        for value in storage_rate_less70_node_detail:
            blockPoolUsedPercent = value['blockPoolUsedPercent']
            if blockPoolUsedPercent > 70: ## 存储率大于70%
                storage_rate_less70_num += 1
                hostList.append(value['infoAddr'])

        dim_value = round(storage_rate_less70_num/all_value,6)*100

        if dim_value > dim_base_detail[dim_key][1] :
            health_detail = "存储节点存储率大于70%的节点占比大于{dim_value}%, 节点详情为：".format(dim_value = dim_base_detail[dim_key][1]) + " ".join(hostList +",请开启快速数据balancer")
    else:
        return None

    weight = dim_base_detail[dim_key][0]
    weightTotal = 0
    for value in dim_base_detail.values():
        weightTotal += value[0]
    weight_percent = round(dim_base_detail[dim_key][0]/ weightTotal,5)

    if dim_value < dim_base_detail[dim_key][1]:
        status_percent = 1
        dim_status = "GOOD"
    elif dim_value > dim_base_detail[dim_key][2]:
        status_percent = 0.8
        dim_status = "BAD"
    else:
        status_percent = 0.6
        dim_status = "CONCERNING"

    expect_score = round(100 * weight_percent,4)

    actual_score = round(100 * weight_percent * status_percent,4)

    if dim_status == "GOOD" :
        health_detail = None

    componentHealthValues.append((board_code, dim_name, dim_status, dim_value, expect_score, actual_score, weight, weight_percent, health_detail, collect_time))
    return (board_code, dim_name, dim_status, dim_value, expect_score, actual_score, weight, weight_percent, health_detail, collect_time)




if __name__ == '__main__':

    ##HDFS监控信息
    response = RequestApi.api_get(hdfs_jmx_url, sessionId=None, param=None)

    namenodeInfo = json.loads(response.content.decode())['beans'][0]

    ##存储基本信息
    hdfs_total_storage = compute_overview(namenodeInfo, "hdfs_total_storage")
    storage_file_num = compute_overview(namenodeInfo, "storage_file_num")
    storage_block_num = compute_overview(namenodeInfo, "storage_block_num")
    storage_total_node = compute_overview(namenodeInfo, "storage_total_node")



    ##存储详情相关指标
    dead_node_num = compute_dim_score(namenodeInfo, "dead_node_num")
    vol_fail_num = compute_dim_score(namenodeInfo, "vol_fail_num")
    storage_balance_rate = compute_dim_score(namenodeInfo, "storage_balance_rate")
    hdfs_block_missing_rateHDFS = compute_dim_score(namenodeInfo, "hdfs_block_missing_rateHDFS")
    bad_block_num = compute_dim_score(namenodeInfo, "bad_block_num")
    hdfs_file_num = compute_dim_score(namenodeInfo, "hdfs_file_num")
    hdfs_storage_rate = compute_dim_score(namenodeInfo, "hdfs_storage_rate")
    storage_rate_less70_node_rate = compute_dim_score(namenodeInfo, "storage_rate_less70_node_rate")
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