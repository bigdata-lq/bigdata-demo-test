"""
目标：完成登录业务层实现
"""
# 导包 unittest Apilogin
import unittest
from etl.testing.yyTest.api.api_login import ApiLogin
from parameterized import parameterized
from etl.testing.yyTest.tools.read_json import ReadJson
#读取数据函数
def get_data(type):
    data = ReadJson("login.json").read_json()
    data = data.get(type)
    # 新建空列表，添加读取json数据
    arrs = []
    arrs.append((data.get("url"),
                 data.get("param"),
                 data.get("expect_result"),
                 data.get("status_code")))
    return arrs

# 新建测试类
class TestLogin(unittest.TestCase):
    # 新建测试方法
    @parameterized.expand(get_data("app_user_login"))
    def test_login(self,url,param,expect_result,status_code):
        s =  ApiLogin().api_post(url,param)
        print("查看响应结果:",s.json())
        self.assertEquals(status_code, s.json()["status"])
        # 断言响应状态码
        # self.assertEquals(200, s.status_code)

    @parameterized.expand(get_data("app_user_sendCaptcha"))
    def test_sendCaptcha(self,url, param, expect_result,status_code):
        s =  ApiLogin().api_post(url,param)
        print("查看响应结果:",s.json())
        self.assertEquals(status_code,s.json()["status"])
        # 断言响应状态码
        # self.assertEquals(200,s.status_code)

    @parameterized.expand(get_data("app_pankoService_historicalTrend"))
    def test_sendCaptcha(self,url, param, expect_result,status_code):
        s =  ApiLogin().api_get(url,param)
        print("查看响应结果:",s.json())

        self.assertEquals(status_code,s.json()["status"])
        # 断言响应状态码
        self.assertEquals(status_code,s.status_code)

if __name__ == '__main__':
    unittest.main()


