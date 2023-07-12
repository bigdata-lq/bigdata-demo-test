
import requests
import time
import sys
params = sys.argv
dateList = params[3].split(",")
interval_time = 60 # 默认间隔
db_name = params[1]
table_name = params[2]
if len(params) > 4 :
    interval_time = params[4]

url = 'https://opskunpeng.yangtuojia.com/api/scrum/partition/migrate'
# 需要注意的是Content-Length参数如果没有，data表单则不会随着请求被发送给服务端，且使用fiddler抓包的过程中，也无法看到data表单
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length':'<calculated when request is sent>'
}

for date_time_str in dateList:
    date_time = time.strftime("%Y-%m-%d", time.strptime(date_time_str, "%Y%m%d"))

    data = {}
    data['endDay'] = '{date_time} 17:28:21'.format(date_time = date_time)
    data['startDay'] = '{date_time} 17:28:21'.format(date_time = date_time)
    data['fromDbName'] = db_name
    data['toDbName'] = db_name
    data['fromTblName'] = table_name
    data['toTblName'] = table_name

    print data
    result = requests.post(url, headers=headers, data=data)
    print result.content.decode('utf-8')
    time.sleep(interval_time)
