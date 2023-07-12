
"""
目标：完成登录接口对象和的封装
"""
# 导包 requests
import requests
from requests.auth import HTTPBasicAuth


class RequestApi(object):

    @staticmethod
    def get_cookies(url, username, password):
        headers = {"Content-Type":"application/json"}
        res = requests.get(url, auth=HTTPBasicAuth(username, password), headers= headers)
        return res.cookies['CLOUDERA_MANAGER_SESSIONID']

    @staticmethod
    def api_post(url,auth, param):
        # headers 定义
        headers = {"Content-Type":"application/json"}
        return requests.post(url, headers=headers, json=param).json()

    @staticmethod
    def api_get(url, sessionId, param):
        # headers 定义
        headers = {"Content-Type":"application/json",
                    "Cookie": "CLOUDERA_MANAGER_SESSIONID={sessionId};".format(sessionId = sessionId)
                   }
        return requests.get(url, headers=headers, params=param)


