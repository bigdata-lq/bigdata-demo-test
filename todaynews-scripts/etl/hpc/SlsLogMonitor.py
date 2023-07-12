from aliyun.log import LogClient
from aliyun.log import GetLogsRequest
import time
import requests


# sls
endpoint = 'cn-hangzhou-intranet.log.aliyuncs.com'
accessKeyId = 'LTAI6QBLDJI5tFkd'
accessKey = 'Fw50Y0iqS6MDY4A1MXhhL6wjBYhssl'

client = LogClient(endpoint, accessKeyId, accessKey)

hosts = ["prod-analytic003", "prod-analytic004","prod-analytic005"]
nowTime = time.time()
nowHour = time.localtime(nowTime).tm_hour

intervalTime = 10
## 0~8 小时 1h 无数据告警 其他时间段 10分钟内无数据告警
if nowHour > 0 and nowHour <= 8:
    intervalTime = 10 * 6

def sendDingdingMsg(host):
    print("{host}机器,10分钟内没有钉钉消息".format(host=host))
    headers = {'X-Requested-With': 'Python requests', 'Content-type': 'application/json; charset=utf-8'}
    msg = "[analytics-logtail] 机器名为: {host}在{intervalTime}分钟内没有采集到数据,请检查logtail的运行情况!!!".format(host= host,
                                                                                            intervalTime = intervalTime )
    context = '{"msgtype": "text","text": {"content": "'+ msg +'"}}'
    try:
        r = requests.post('https://oapi.dingtalk.com/robot/send?access_token=3dec2ec8f5e9a47d438dcb0dda93e24b92ffbcb4718436290d7fe49d199b9dbf',
                          data=context.encode('utf8'), headers=headers, timeout=8)
        r.raise_for_status() # 如果响应状态码不是 200，就主动抛出异常
    except requests.RequestException as e:
        print(e)


# 使用client的方法来操作日志服务
for host in hosts:
    request = GetLogsRequest("ytprod", "analytic-applog-prod", fromTime=int(nowTime-intervalTime*60), toTime=int(nowTime), topic='', query="* and __tag__:__hostname__: {host}".format(host = host), line=5, offset=0, reverse=False)
    res = client.get_logs(request)
    if res.get_count() == 0:
        sendDingdingMsg(host)
    else:
        print("success")


