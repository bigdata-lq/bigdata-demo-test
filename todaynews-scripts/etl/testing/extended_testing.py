from etl.testing.util.request_util import *
from etl.testing.data.json_util import dumpJson
import unittest
from etl.testing.HTMLTestRunner import HTMLTestRunner


server_url = "http://dev-ya.yangtuojia.com:8080"
extended_data_path = "./data/extendedConfig.json"

class ExtendedTest(unittest.TestCase):

    def setUp(self):
        ## 获取token
        self.case_json_map = dumpJson(extended_data_path)


    def extended_update_success(self):
        # 用例加载
        case_json = self.case_json_map['extended_update_success']
        request_url = server_url + case_json['request_url']
        print("start testing request url: {request_url}".format(request_url = request_url))

        response = post(url=request_url, params= case_json['data_use_case']['param_object'])
        realResCode = response['code'] # 真实值
        expectResCode = case_json['data_use_case']['code'] # 期望值
        # 断言
        self.assertEqual(realResCode, expectResCode)

    def extended_update_error(self):
        # 用例加载
        case_json = self.case_json_map['extended_update_error']
        request_url = server_url + case_json['request_url']
        print("start testing request url: {request_url}".format(request_url = request_url))

        response = post(url=request_url, params= case_json['data_use_case']['param_object'])
        realResCode = response['code'] # 真实值
        expectResCode = case_json['data_use_case']['code'] # 期望值
        # 断言
        self.assertEqual(realResCode, expectResCode)

    def extended_search_sucess(self):
        # 用例加载
        case_json = self.case_json_map['extended_search_sucess']
        request_url = server_url + case_json['request_url']
        print("start testing request url: {request_url}".format(request_url = request_url))

        response = get(url=request_url, params_obj= case_json['data_use_case']['param_object'])
        realResCode = response['code'] # 真实值
        expectResCode = case_json['data_use_case']['code'] # 期望值
        # 断言
        self.assertEqual(realResCode, expectResCode)



if __name__ == '__main__':

    # 初始化测试上下文
    suite = unittest.TestSuite()
    # suite.addTest(unittest.makeSuite(ExtendedTest))
    suite.addTest(ExtendedTest("extended_update_success"))
    suite.addTest(ExtendedTest("extended_update_error"))
    suite.addTest(ExtendedTest("extended_search_sucess"))
    # 存放路径在E盘目录下
    filepath='./pyresult.html'
    fp=open(filepath,'wb')
    #定义测试报告的标题与描述
    runner = HTMLTestRunner(stream=fp,title=u'扩展字段自动化测试报告',description=u'扩展字段功能自动化测试')
    runner.run(suite)
    fp.close()