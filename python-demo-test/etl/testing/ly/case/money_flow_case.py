import unittest

from parameterized import parameterized
from etl.testing.ly.utils.read_json import ReadJson
from etl.testing.ly.utils.request_api import RequestApi

moneyFlowData = ReadJson("money_flow.json")


class MoneyFlow(unittest.TestCase):

    @parameterized.expand(moneyFlowData.getCaseByType("jj_001"))
    def test_jj_001(self, url, param, expect_result, status_code, name):
        s =  RequestApi().api_get(url,param)
        self.print(s.json())
        ##断言
        self.assertEquals(status_code, s.json()["status"])


    @parameterized.expand(moneyFlowData.getCaseByType("jj_002"))
    def test_jj_002(self,url, param, expect_result,status_code, name):
        
        s =  RequestApi().api_get(url,param)
        self.print(s.json())
        ##断言
        self.assertEquals(status_code,s.json()["status"])


    def print(self, res):
        print("查看响应结果:", res)




if __name__ == '__main__':
    unittest.main()