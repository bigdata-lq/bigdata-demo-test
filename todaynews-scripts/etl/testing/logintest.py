# 导包
import requests
import json
import unittest

#定义接口请求设置一个变量名称

domain_prefix = "http://8.129.162.225:8080/system/user"
token_url = "/login"
getRouters_url = "/getRouters"
treeselect_url = "/system/dept/treeselect"



# 定义登录获取动态token方法

def _getToken_(token_url):
    #定义请求头和入参
    headers = {"Content-Type":"application/json"}
    header={"Authorization", "{{Authorization}}"}
    params = {

        "username":"18358521853",
        "Code":"1234",
        "password":"123456",
        "uuid":"84f9e822e8524417830e1b3f9ccb0f96"

    }
    # request获取post请求返回token
    response = requests.post(url=token_url,headers=headers, json=params)
    #
    # # 解析response转化为json对象
    # resobject = json.loads(response.content)
    # if resobject['code'] == 401:
    #     print(resobject['code'])
    #     return
    # token = resobject['token']
    # print(token)
    # return token



class Test_Dict(unittest.TestCase):

    #获取token
    def setUp(self):
        self.token = _getToken_(domain_prefix + token_url)

        #普通url
    def test_list_url_(self):
        if self.token == None:
            self.token = _getToken_(domain_prefix + token_url)
        headers ={'token':self.token}
        #发送请求获取token
        response=requests.get(url= domain_prefix +treeselect_url,headers=headers,params=None)
        #解析response 转化为json对象
        resobject = json.loads(response.content)
        print('打印返回信息：{}'.format(resobject))
        #获取状态码
        status = resobject["status"]
        print('打印状态码信息：{}'.format(status))
        #断言
        self.assertEqual(status,200,"listGroup_url断言失败")
        pass
    # 普通url
    def test_queryUserOptional_url_(self):
        # 如果token失效,重新获取
        if self.token == None:
            self.token = _getToken_(domain_prefix + token_url)

        headers = {"X-token" : self.token}
        # 发送请求获取token
        response = requests.get(url= domain_prefix + treeselect_url,headers=headers, params=None)
        # 解析response转化s为json对象
        resObject = json.loads(response.content)
        print("打印返回信息:{}".format(resObject))
        # 获取状态码
        status = resObject["status"]
        print("打印状态码信息:{}".format(status))
        # 断言
        self.assertEqual(status, 200, "treeselect_url断言失败")

        pass

    #
    # #添加分组  查询分组  删除分组
    # def test_complex_case_(self):
    #
    #     #如果token失效，重新获取
    #     if self.token == None:
    #         self.token=_getToken_(damain_prefix + token_url)
    #     headers = {"X-token": self.token}
    #     group_name = "hello9"
    #
    #     #新增自选股分组
    #     print("第一步新增名称为{}自选股分组-------------".format(group_name))
    #     addGroup_param = {"name":group_name}
    #     # 发送请求获取token
    #     response = requests.post(url=domain_prefix+addGroup_url,headers = headers,json=addGroup_param)
    #     resobject = json.loads(response.content)
    #     print("打印返回信息：{}".format(resobject))
    #     # 获取状态码
    #     status = resobject["status"]
    #     print("打印状态码信息:{}".format(status))
    #     #断言
    #     self.assertEqual(status,200,"addGroup_url断言失败")
    #
    #     #获取自选股列表
    #     print("第二部获取自选股列表-------------------")
    #     response = requests.get(url=domain_prefix+listGroup_url,headers= headers,params=None)
    #     #解析response转化为json对象
    #     resobject=json.loads(response.content)
    #     print("打印返回信息：{}".format(resobject))
    #     #获取状态码
    #     status = resobject["status"]
    #     print("打印状态码信息：".format(status))
    #     #断言
    #     self.assertEqual(status,200,"listGroup_url断言失败")
    #
    #     #删除名字叫hello的自选股信息
    #
    #     #获name为hello自选股id
    #     print("第三步删除名字叫{}自选股-----------".format(group_name))
    #
    #     group_id = None
    #     for groupobject in resobject["data"]:
    #         if group_name == groupobject["name"]:
    #             group_id=groupobject["id"]
    #             print("打印{}自选股的id为{}".format(group_name,group_id))
    #     deletedGroup_param = {"id":group_id}
    #     response = requests.post(url=domain_prefix +deleteGroup_url,headers=headers,json= deletedGroup_param)
    # #解析json
    #     resobject =json.loads(response.content)
    #     print("打印返回信息：".format(resobject))
    #     #获取状态码
    #     status = resobject["status"]
    #     print("打印状态码信息：{}".format(status))
    #     #断言
    #     self.assertEqual(status,200,"deletedGroup_ur;断言失败")
    #     pass
    #
    #     #再次获取自选股列表
    #     print("第四步再次获取自选股列表------------")
    #     response = requests.get(url=domain_prefix+listGroup_url,headers=headers,params=None)
    #     #解析response转化为json对象
    #     resobject = json.loads(response.content)
    #     print("打印返回信息：".format(resobject))
    #
    #     #获取状态码
    #     status = resobject["status"]
    #     print("打印状态码信息：".format(status))
    #
    #     #断言
    #     self.assertEqual(status,200,"再次listGroup_url断言失败")
    #     pass

    def tearDown(self) :
        pass
if __name__ == '__main__':
    # unittest.main
    print(1)





