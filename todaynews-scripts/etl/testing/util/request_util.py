## -*-coding:utf-8 -*-
#---------
# Name: post/get请求工具类
#---------

import requests
import json
import urllib


# 用于header中带有access_token的情况

# get请求
def get(url, token=None, headers={}, params_obj={}):
    if token is not None:
        headers['Authorization'] = 'Bearer ' + token
    params = urllib.parse.urlencode(params_obj).encode('utf-8')
    response = requests.get(url + "?" + str(params, 'utf-8'), headers=headers)
    return to_response(response)

# post请求 入参为application/json这种情况
def post(url, token=None,
         headers={'Content-type': 'application/json;charset=UTF-8', 'Accept': 'application/json, text/plain'},
         params={}):
    if token is not None:
        headers['Authorization'] = 'Bearer ' + token
    response = requests.post(url, data=json.dumps(params),
                             headers=headers)
    return to_response(response)

# 将get post请求的结果(byte[])转成对象
def to_response(response):
    # 得到的是byte[]
    byte_content = response.content.decode('utf-8-sig')
    # 转成对象
    return json.loads(byte_content)


if __name__ == '__main__':
    response = get(url= 'http://dev-ya.yangtuojia.com:8080/admin/extended/list',params_obj={'name':'item'})
    print(response)