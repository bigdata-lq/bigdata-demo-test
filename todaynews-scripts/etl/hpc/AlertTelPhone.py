import requests
import time



phoneList = ['13173699826', '']
phoneUrl = """
https://ytgw.hipac.cn/pub/voiceAlarm?param=FAULT_CODE:10,APP:大数据集群,ERR_MSG:进程出现问题&templateId=TP18111328&mobile={mobile}&orderNo={orderNo}
"""

def sendPhone():
    for phoneNum in phoneList:
        orderNo = 'bigdata'+ str(int(round(time.time() * 1000)))
        url = phoneUrl.format(mobile = phoneNum, orderNo = orderNo)
        print(url)
        respose = requests.get(url)
        print(str(respose.status_code)  + ":" + str(respose.text))
    return

sendPhone()
## 拨打两次
time.sleep(300)

sendPhone()