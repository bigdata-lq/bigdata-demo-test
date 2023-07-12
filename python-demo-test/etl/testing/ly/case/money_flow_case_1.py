import unittest
import warnings

from etl.testing.ly.libs.ddt import *
from etl.testing.ly.utils.read_json import ReadJson
from etl.testing.ly.utils.request_api import RequestApi

moneyFlowData = ReadJson("money_flow_1.json").jsonCase
# print(type(moneyFlowData))

@ddt
class money_flow(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        import urllib3
        urllib3.disable_warnings()
        warnings.simplefilter('ignore', ResourceWarning)
        cls.globals = globals()
        initData = ReadJson("init.json").jsonCase
        for key in initData:
            cls.globals[key] = initData[key]
        print("初始化测试用例、全局参数")



    @data(*moneyFlowData)
    def test(self,case):
        print("\n")

        case_name = case["case_name"]
        desc = case["desc"]
        url = case["url"]
        param = case["param"]
        expect_result = case["expect_result"]
        status_code = case["status_code"]
        responce_param = case["responce_param"]
        method = case["method"]
        print("当前执行的用例为: {}, 用例描述为：{}".format(case_name,desc))
        print("请求的url为：" + str(url))
        print("(替换前)请求的入参为：" + str(param))

        ##替换case中参数
        for key in param:
            if str(param[key]).startswith("$."):
                param[key] = self.globals[key]

        ## 发送用例请求
        responce = None
        if method == 'post':
            responce =  RequestApi().api_post(url,param).json()
        else:
            responce =  RequestApi().api_get(url,param).json()

        res = None

        ## 校验返回值类型,如果是dict,取出整条，如果是list,取第一条
        if isinstance(responce["data"], list) and len(responce["data"]):
            res = responce["data"][0]
        elif  isinstance(responce["data"], dict):
            res = responce["data"]
        else:
            pass

        print("(替换后)请求的入参为：" + str(param))
        print("返回的数据类型为: {},返回的一条数据为：{}".format(type(responce["data"]), str(res)))


        ##结果值写入全局变量
        for key in responce_param:
            if res :
                self.globals[key] = res[key]
        self.print(responce)

        ##断言
        self.assertEqual(status_code, responce["status"])

    def print(self, res):
        print("请求响应结果为:{}".format(res))

if __name__ == '__main__':
    unittest.main()

