
"""
目标：完成登录接口对象和的封装
"""
# 导包 requests
import requests

class RequestApi(object):

    ## post请求
    def api_post(self,url, param):
        # headers 定义
        headers = {"Content-Type":"application/json"}
        return requests.post(url,headers=headers,json=param)

    ## get请求
    def api_get(self, url, auth, param):
        # headers 定义
        headers = {"Content-Type":"application/json"}
        return requests.get(url,headers=headers, auth= auth,params=param)


