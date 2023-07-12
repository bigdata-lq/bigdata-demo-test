from operations.request_util import RequestApi
import json
import datetime
from operations.mysql_util import MysqlUtil

hostList = [
    "prod-hadoop-slave001", "prod-hadoop-slave002", "prod-hadoop-slave003","prod-hadoop-slave004", "prod-hadoop-slave005", "prod-hadoop-slave006",
    "prod-hadoop-slave007", "prod-hadoop-slave008", "prod-hadoop-slave009","prod-hadoop-slave010", "prod-hadoop-slave011", "prod-hadoop-slave012",
    "prod-hadoop-slave014", "prod-hadoop-slave015","prod-hadoop-slave016", "prod-hadoop-slave017"
]

dirList = ["/alidata1/", "/alidata2/", "/alidata3/", "/alidata4/", "/alidata5/", "/alidata6/", "/alidata7/", "/alidata8/",
           "/alidata9/", "/alidata10/", "/alidata11/", "/alidata12/", "/alidata13/", "/alidata14/", "/alidata15/", "/alidata16/"]

jmx_url = "http://{hostName}:50075/jmx"


for hostName in hostList:
    response = RequestApi.api_get(jmx_url.format(hostName = hostName), None, None)
    for metric in json.loads(response.content.decode())['beans']:
        if metric["name"].startswith("Hadoop:service=DataNode,name=FSDatasetState"):
            storageInfo = metric["StorageInfo"]
            for dir in dirList:
                if  storageInfo.find(dir) < 0:
                    print(hostName, dir)





