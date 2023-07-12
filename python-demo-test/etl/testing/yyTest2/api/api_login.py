
"""
目标：完成登录接口对象和的封装
"""
# 导包 requests
import requests
#新建类 登录接口对象
class ApiLogin(object):
    # 新建方法 登录方法
    def api_post_login(self,url,phone,Code):
        # headers 定义
        headers = {"Content-Type":"application/json"}
        #data 定义
        data = {"phone":phone,"Code":Code}
        #调用post并返回响应对象
        return requests.post(url,headers=headers,json=data)

"""
提示：
    url，phone，code:最后都需要从data数据文件读取出来，做参数化使用，所以这里使用动态传参
"""