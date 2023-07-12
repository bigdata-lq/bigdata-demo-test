"""
目标：完成登录业务层实现
"""
# 导包 unittest Apilogin
import unittest
from etl.testing.yyTest.api.api_login import ApiLogin
from parameterized import parameterized
from etl.testing.yyTest.tools.read_json import ReadJson
#读取数据函数
def get_data():
    data = ReadJson("login.json").read_json()
    # 新建空列表，添加读取json数据
    arrs = []
    arrs.append((data.get("url"),
                 data.get("phone"),
                 data.get("Code"),
                 data.get("expect_result"),
                 data.get("status_code")))
    return arrs

# 新建测试类
class TestLogin(unittest.TestCase):
    # 新建测试方法
    @parameterized.expand(get_data())
    def test_login(self,url,phone,Code,expect_result,status_code):
        s =  ApiLogin().api_post_login(url,phone,Code)
        # 调试使用
        print("查看响应结果:",s.json())
        # 断言响应状态码
        self.assertEquals(status_code,s.status_code)

if __name__ == '__main__':
    unittest.main()


