## -*-coding:utf-8 -*-
#---------
# Name:lq
# Message: 解析hadoop xml hdfs参数
#---------
import requests
import json
import xmltodict

## dataNodeUrl 参数
datanode_url = "http://prod-hadoop-slave001:50075/conf"

responce = requests.get(datanode_url,params={}, headers = {'Content-type': 'text/plain; version=0.0.4;charset=utf-8','Accept': '*/*'})
datanodeConf = str(responce.content, encoding = "utf-8")


#定义xml转json的函数
def xmltojson(xmlstr):
    #parse是的xml解析器
    xmlparse = xmltodict.parse(xmlstr)
    #json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式。
    #dumps()方法的ident=1，格式化json
    jsonstr = json.dumps(xmlparse,indent=1)
    return jsonstr


datanodeConf = xmltojson(datanodeConf)
# print(datanodeConf)

dict = {}

for conf in json.loads(datanodeConf)['configuration']['property']:
    name = conf['name']
    value = conf['value']
    source = conf['source']
    if name == None or value == None or source == None :
        continue
    if source in dict :
        dict[source] = dict.get(source) + '\r\n' + (name + " : " + value)
    else:
        dict[source] = name + " : " + value

for key in dict:
    print('----' + key +':')
    print(dict[key])

    print("------------------------------")
    print("------------------------------")
    print("------------------------------")












